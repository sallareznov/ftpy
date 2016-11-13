#!/usr/bin/env python3

import logging
import ftplib
import sys
import argparse
import os.path
import cli
import time
import constants
import itertools
import datetime
import os

def parseArguments():
    """Parses command line arguments and returns a Namespace object
    if successful, an error otherwise
    """
    parser = cli.buildParser()
    return parser.parse_args()

def isNew(path, timestampBeforeRefresh):
    """Returns True if the entry has been created, modified or delete between
    two refreshes
    """
    return (os.path.getctime(path) > timestampBeforeRefresh)

def addFolder(folderState, ftpClient):
    """Add a folder to the server"""
    for root, dirs, files in folderState:
        ftpClient.mkd(root)
        for filename in files:
            filepath = os.path.join(root, filename)
            ftpClient.storbinary("STOR " + filepath, open(filepath, "rb"))

def handleFolder(folder, foldersBeforeRefresh, ftpClient):
    """Handles a folder in the synchronization process"""
    if (folder in foldersBeforeRefresh):
        rmFolder(folder, ftpClient)
        if (os.path.exists(folder)):
            if (debugMode):
                logging.info("Folder modified: " + folder)
            addFolder(os.walk(folder), ftpClient)
        else:
            if (debugMode):
                logging.info("Folder deleted: " + folder)
    else:
        if (debugMode):
            logging.info("Folder added: " + folder)
        addFolder(os.walk(folder), ftpClient)

def handleFile(filepath, filesBeforeRefresh, ftpClient):
    """Handles a file in the synchronization process"""
    if (filepath in filesBeforeRefresh):
        if (os.path.exists(filepath)):
            ftpClient.delete(filepath)
        else:
            ftpClient.storbinary("STOR " + filepath, open(filepath, "rb"))
    else:
        ftpClient.storbinary("STOR " + filepath, open(filepath, "rb"))

def isAlreadyHandled(folder, handledFolders):
    """Returns True if the folder is already added to the server"""
    for handledFolder in handledFolders:
        if (folder.startswith(handledFolder)):
            return True
    return False

def rmFolder(folder, ftpClient):
    """Removes a folder from the server"""
    try:
        ftpClient.rmd(folder)
    except Exception:
        for entry in ftpClient.nlst(folder):
            try:
                ftpClient.delete(entry)
            except Exception:
                rmFolder(entry, ftpClient)
        rmFolder(folder, ftpClient)

if (__name__ == "__main__"):
    # parsing and retrieving command-line arguments
    namespace = parseArguments()
    localFolder = namespace.__getattribute__(constants.LOCAL_FOLDER_OPTION)
    logFile = namespace.__getattribute__(constants.LOG_FILE_OPTION)
    ftpServerUrl = namespace.__getattribute__(constants.FTP_SERVER_URL_OPTION)
    username = namespace.__getattribute__(constants.USERNAME_OPTION)
    password = namespace.__getattribute__(constants.PASSWORD_OPTION)
    refreshFrequency = namespace.__getattribute__(constants.REFRESH_FREQUENCY_OPTION)
    maxDepth = namespace.__getattribute__(constants.MAX_DEPTH_OPTION)
    debugMode = namespace.__getattribute__(constants.DEBUG_OPTION)

    # creating and configuring
    ftpClient = ftplib.FTP(ftpServerUrl)
    ftpClient.login(user=username, passwd=password)
    ftpClient.set_debuglevel(1)

    # adding the folder to the server
    addFolder(os.walk(localFolder), ftpClient)

    # configuring the logger
    logging.basicConfig(filename=logFile,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    while (True):
        foldersBeforeRefresh = [x[0] for x in os.walk(localFolder)]
        filesBeforeRefresh = sum([x[2] for x in os.walk(localFolder)], [])
        handledFolders = []
        timestampBeforeRefresh = time.time()
        time.sleep(refreshFrequency)
        folderState = os.walk(localFolder)
        for root, dirs, files in folderState:
            if (isNew(root, timestampBeforeRefresh) and not isAlreadyHandled(root, handledFolders)):
                handleFolder(root, foldersBeforeRefresh, ftpClient)
                handledFolders.append(root)
            for filename in files:
                filepath = os.path.join(root, filename)
                if (isNew(filepath, timestampBeforeRefresh)):
                    handleFile(filepath, filesBeforeRefresh, ftpClient)
