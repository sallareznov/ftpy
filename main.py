#!/usr/bin/env python3

import logging
from ftplib import FTP
import sys
import argparse
import os.path
import cli
import time
import constants

def parseArguments():
    """Parses command lines arguments and returns a Namespace object
    if successful, an error otherwise
    """
    parser = cli.buildParser()
    return parser.parse_args()

if (__name__ == "__main__"):
    namespace = parseArguments()
    print(namespace._get_args)
    localFolder = namespace.__getattribute__(constants.LOCAL_FOLDER_OPTION)
    logFile = namespace.__getattribute__(constants.LOG_FILE_OPTION)
    ftpServerUrl = namespace.__getattribute__(constants.FTP_SERVER_URL_OPTION)
    username = namespace.__getattribute__(constants.USERNAME_OPTION)
    password = namespace.__getattribute__(constants.PASSWORD_OPTION)
    refreshFrequency = namespace.__getattribute__(constants.REFRESH_FREQUENCY_OPTION)
    maxDepth = namespace.__getattribute__(constants.MAX_DEPTH_OPTION)
    debugMode = namespace.__getattribute__(constants.DEBUG_OPTION)

    ftpClient = FTP(ftpServerUrl)
    ftpClient.login(user=username, passwd=password)

    for root, dirs, files in os.walk(localFolder):
        print("(" + root + ", " + dirs + ", " + files + ")")
    while (True):
        time.sleep(refreshFrequency)
