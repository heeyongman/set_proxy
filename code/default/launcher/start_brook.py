# coding:utf-8

import os
import sys
import logging
import traceback

current_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.abspath(os.path.join(current_path, os.pardir, os.pardir, os.pardir))

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.FileHandler(filename=log_path + '\\get_proxy.log', encoding='utf-8')
logging.basicConfig(filename=log_path + '\\get_proxy.log', level=logging.DEBUG, format=LOG_FORMAT)

server_file = current_path + "\\server.dat"

try:
    with open(server_file, mode='r') as server_file:  # , py2中没有encoding='utf-8'
        # server = server_file.read()
        server = server_file.readline().strip()
        pwd = server_file.readline()
except:
    logging.error(traceback.format_exc())
    sys.exit(0)
# print("server:" + server + "pwd:" + pwd)

cmd = r'""%s\brook_windows_386.exe" client -l 127.0.0.1:1080 -i 127.0.0.1 -s %s -p %s"' \
      % (current_path, server, pwd)

os.system(cmd)
logging.error("brook boot failed!")

