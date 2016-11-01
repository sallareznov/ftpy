#!/usr/bin/env python3

import logging
from ftplib import FTP
import sys
import argparse
import os.path
import cli

def parseArguments():
    parser = cli.buildParser()
    return parser.parse_args()

if (__name__ == "__main__"):
    namespace = parseArguments()
    localFolder = namespace.__getattribute__("local_folder")
    logFile = namespace.__getattribute__("log_file")
    ftpServerUrl = namespace.__getattribute__("ftp_server_url")
    username = namespace.__getattribute__("username")
    password = namespace.__getattribute__("password")
    debugMode = namespace.__getattribute__("debug")
    print(namespace._get_args)
    refreshFrequency = namespace.__getattribute__("refresh_frequency")
    maxDepth = namespace.__getattribute__("max_depth")

    ftpClient = FTP(ftpServerUrl)
    ftpClient.login(user=username, passwd=password)
    print(ftpClient.pwd())
