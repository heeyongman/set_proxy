# coding:utf-8

import os
import sys
import logging
import traceback
from set_proxy import set_proxy

current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_path, os.pardir))
data_path = os.path.abspath(os.path.join(root_path, os.pardir, os.pardir, 'data'))
data_launcher_path = os.path.join(data_path, 'launcher')
python_path = os.path.join(root_path, 'python27', '1.0')
log_path = os.path.abspath(os.path.join(current_path, os.pardir, os.pardir, os.pardir))
noarch_lib = os.path.abspath(os.path.join(python_path, 'lib', 'noarch'))
sys.path.append(noarch_lib)

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(filename=log_path+'\\get_proxy.log', level=logging.DEBUG, format=LOG_FORMAT)

has_desktop = True

platform_lib = os.path.join(python_path, 'lib', 'win32')
sys.path.append(platform_lib)


def main():

    logging.info("-------------------------------------------------------------------")
    logging.info("[step1]:start setting proxy...")
    # subprocess.Popen('cmd/c start ' + cmd_line, shell=True)
    try:
        set_proxy()
        logging.info("[step2]:start sys_tray...")
        print("[step2]:start sys_tray...")
        cmd_line = '%s\\python.exe %s\\win_tray.py' % (python_path, current_path)
        os.system('cmd/c ' + cmd_line)
        logging.info("started serve_forever")

    except Exception:
        logging.error(traceback.format_exc())


if __name__ == '__main__':
    main()
