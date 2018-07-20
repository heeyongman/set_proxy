# coding=utf-8
import os
import sys
import re
import subprocess
import requests
from modify_hosts import execute
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
carrier = "1"  # 0:unicom/mobile,1:telecom

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(filename=log_path + '\\get_proxy.log', level=logging.DEBUG, format=LOG_FORMAT)


def get_page(url, charset):
    try:
        res = requests.get(url).content.decode(charset).encode('utf-8')
        return res
    except Exception:
        logging.error(traceback.format_exc())
        bubble.startBubble('GetProxy', u'连接服务器异常，请保持网络畅通', 3)
        sys.exit(0)


def create_datafile():
    global carrier
    if not status:
        # 创建快捷方式
        subprocess.call(["Wscript.exe", "//E:JScript", curr_path + "\\create_shortcut.js"], shell=False)
        # 获取运营商
        ip_url = "http://www.ip138.com/ips1388.asp"
        ip_page = get_page(ip_url, 'gb2312')
        #  encoding='utf-8'
        with open(data_file_path, mode='w') as data_file:
            if '电信' in ip_page:
                data_file.write("1")
                carrier = "1"
            else:
                data_file.write("0")
                carrier = "0"
        # 修改hosts
        execute()
    else:
        with open(data_file_path, mode='r') as read_file:
            carrier = read_file.read()


def set_proxy():
    create_datafile()
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

    if not server or len(server) < 2:
        logging.error("获取Server信息失败！")
        bubble.startBubble('GetProxy', u'获取Server失败，请保持网络畅通', 3)
        sys.exit(0)

    pwd_re = re.compile('DOUBI.{10}')
    pwd = re.findall(pwd_re, page)
    # print("Server0(联通):%s\tServer1(电信):%s".decode('utf-8').encode(sys_type) % (server[0], server[1]))
    logging.info((server, pwd[0]))

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
    logging.info("自动部署已完成")


if __name__ == '__main__':
    set_proxy()
