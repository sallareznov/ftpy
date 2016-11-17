import argparse
import constants

def buildParser():
    """Builds the parser"""
    parser = argparse.ArgumentParser(description="saves and synchronizes a local folder with a FTP server")
    parser.add_argument(constants.LOCAL_FOLDER_OPTION, help="the local folder to save and synchronize with the server")
    parser.add_argument(constants.LOG_FILE_OPTION, help="the log file")
    parser.add_argument(constants.FTP_SERVER_URL_OPTION, help="the url of the server")
    parser.add_argument(constants.USERNAME_OPTION, help="the username of the account in the server")
    parser.add_argument(constants.PASSWORD_OPTION, help="the password of the account in the server")
    parser.add_argument("--" + constants.REFRESH_FREQUENCY_OPTION, type=int, default=3, help="the refresh frequency (default=1)")
    parser.add_argument("--" + constants.MAX_DEPTH_OPTION, type=int, default=6, help="the maximum level of subfolders to handle (default=6)")
    parser.add_argument("--" + constants.DEBUG_OPTION, action="store_true", help="activate the debug mode (default=True)")
    return parser
