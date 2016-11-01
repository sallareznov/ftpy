# ftpy

`ftpy` is a tool for saving and synchronization of a local folder with a FTP server.

## Usage

```
usage: main.py [-h] [--refresh_frequency REFRESH_FREQUENCY]
               [--max_depth MAX_DEPTH] [--debug]
               local_folder log_file ftp_server_url username password

saves and synchronizes a local folder with a FTP server

positional arguments:
  local_folder          the local folder
  log_file              the log file
  ftp_server_url        the url of the FTP server
  username              the username of the account in the FTP server
  password              the password of the account in the FTP server

optional arguments:
  -h, --help            show this help message and exit
  --refresh_frequency REFRESH_FREQUENCY
                        the refresh frequency (default=1)
  --max_depth MAX_DEPTH
                        the maximum level of subfolders to handle (default=6)
  --debug               activate the debug mode (default=True)
  ```
