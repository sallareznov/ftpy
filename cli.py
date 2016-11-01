import argparse

def buildParser():
    parser = argparse.ArgumentParser(description="saves and synchronizes a local folder with a FTP server")
    parser.add_argument("local_folder", help="the local folder")
    parser.add_argument("log_file", help="the log file")
    parser.add_argument("ftp_server_url", help="the url of the FTP server")
    parser.add_argument("username", help="the username ???")
    parser.add_argument("password", help="the password ???")
    parser.add_argument("--refresh-frequency", type=int, default=1, help="the refresh frequency")
    parser.add_argument("--max-depth", type=int, default=6, help="the maximum level of subfolders to handle")
    parser.add_argument("--debug", action="store_true")
    return parser
