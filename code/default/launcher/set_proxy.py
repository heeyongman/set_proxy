# coding=utf-8
import os
import sys
import re
import subprocess
import requests
import ping
# from modify_hosts import execute
import logging
import traceback
from bubble import bubble

sys_type = sys.getfilesystemencoding()

# 判断数据文件是否存在
curr_path = os.path.dirname(os.path.abspath(__file__))
# data_file_path = curr_path + "\\data"
data_file_path = os.path.join(curr_path, os.pardir, os.pardir, os.pardir, 'data')
log_path = os.path.abspath(os.path.join(curr_path, os.pardir, os.pardir, os.pardir))
status = os.path.exists(data_file_path)
sys.path.append(curr_path)
carrier = "0"  # min_delay_server

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.FileHandler(filename=log_path+'\\get_proxy.log', encoding='utf-8')
logging.basicConfig(filename=log_path + '\\get_proxy.log', level=logging.DEBUG, format=LOG_FORMAT)


def get_page(url, charset):
    try:
        res = requests.get(url).content.decode(charset).encode('utf-8')
        return res
    except Exception:
        logging.error(traceback.format_exc())
        bubble.startBubble('GetProxy', u'连接服务器异常，请保持网络畅通', 3)
        sys.exit(0)


def modify_hosts():
    os.system(curr_path+'\\modify_hosts.bat')


def modify_shortcut_hosts():
    global carrier
    if not status:
        # 创建快捷方式
        subprocess.call(["Wscript.exe", "//E:JScript", curr_path + "\\create_shortcut.js"], shell=False)
        # 修改hosts
        modify_hosts()
    else:
        with open(data_file_path, mode='r') as read_file:
            carrier = read_file.read()


def get_min_server(server):
    # get min_delay_server
    global status
    delay = []
    for s in server:
        try:
            d = ping.do_one(s, timeout=2, psize=64)
            delay.append(2 if d is None else d)
        except:
            logging.error(traceback.format_exc())
            bubble.startBubble('GetProxy', u'连接服务器异常，请保持网络畅通', 3)
            sys.exit(0)

    min_server = str(delay.index(min(delay)))
    logging.info("min_server_num: %s" % min_server)
    logging.info("min_server: %s" % server[int(min_server)])
    #  encoding='utf-8'
    with open(data_file_path, mode='w') as data_file:
        data_file.write(min_server)
        global carrier
        carrier = min_server


def set_proxy():
    modify_shortcut_hosts()
    bubble.startBubble("GetProxy", u"获取Server中...", 1)
    # notifier("GetProxy", "获取Server中...".decode('utf-8').encode(sys_type), 3)
    logging.info("获取Server中...")
    # print("获取Server中...".decode('utf-8').encode(sys_type))
    # 获取Server
    ser_url = "https://doub.io/sszhfx/"
    page = get_page(ser_url, 'utf-8')

    # <strong>服务器栏的格式为：IP:端口，即 nyc1.brookfree.pw:7000</strong>
    server_re = re.compile('(?<=即 ).*(?=</strong)')
    server = re.findall(server_re, page)
    logging.info(server)

    if not server:
        logging.error(u"获取Server信息失败！")
        bubble.startBubble('GetProxy', u'获取Server失败，请保持网络畅通', 3)
        sys.exit(0)

    pwd_re = re.compile('DOUBI.{10}')
    pwd = re.findall(pwd_re, page)
    # print("Server0(联通):%s\tServer1(电信):%s".decode('utf-8').encode(sys_type) % (server[0], server[1]))
    logging.info((server, pwd[0]))

    # 获取最低延的server
    new_server = [s[0:s.index(":")] for s in server]
    get_min_server(new_server)

    # 执行文件的绝对路径
    start_file = curr_path + "\\start_brook.vbs"
    config_file = curr_path + "\\start_brook.cmd"

    # with open(start_file, encoding='utf-8') as f:
    #     old_line = f.read()
    # 修改
    new_line = "%s\\\\brook_windows_386.exe client -l 127.0.0.1:1080 -i 127.0.0.1 -s %s -p %s" \
               % (curr_path.replace("\\", "\\\\"), server[int(carrier)], pwd[0])
    # 写入文件
    with open(config_file, mode='w') as config_file:  # , encoding='utf-8'
        config_file.write(new_line)

    # 执行脚本
    cmd = 'taskkill /F /IM brook_windows_386.exe'
    os.system(cmd)
    os.startfile(start_file)
    # print("\n恭喜你可以访问真正的互联网了！".decode('utf-8').encode(sys_type))
    # end = raw_input("请按回车键继续...".decode('utf-8').encode(sys_type))
    bubble.startBubble('GetProxy', u'自动部署已完成，Enjoy! :)')
    # notifier('GetProxy', '自动部署已完成，Enjoy! :)'.decode('utf-8').encode(sys_type), 3)
    logging.info(u"自动部署已完成")


if __name__ == '__main__':
    set_proxy()
