#!/usr/bin/env python3
# coding=utf-8
# apply to python3
import os
import sys
import re
import requests
import ping3
import logging
import traceback

sys_type = sys.getfilesystemencoding()

# 判断数据文件是否存在
curr_path = os.path.dirname(os.path.abspath(__file__))
# data_file_path = curr_path + "\\data"
data_file_path = os.path.join(curr_path, 'data')
sys.path.append(curr_path)
carrier = "0"  # min_delay_server

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.FileHandler(filename=curr_path + os.sep + 'get_proxy.log', encoding='utf-8')
logging.basicConfig(filename=curr_path + os.sep + 'get_proxy.log', level=logging.DEBUG, format=LOG_FORMAT)


def get_page(url, charset):
    try:
        res = requests.get(url).content.decode(charset)
        return res
    except Exception:
        logging.error(traceback.format_exc())
        sys.exit(0)


def get_min_server(server):
    # get min_delay_server
    global status
    delay = []
    for s in server:
        try:
            d = ping3.ping(s, timeout=2)
            delay.append(2 if d is None else d)
        except:
            logging.error(traceback.format_exc())
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
    logging.info("获取Server中...")
    # 获取Server
    ser_url = "https://doub.io/sszhfx/"
    page = get_page(ser_url, 'utf-8')

    # <strong>服务器栏的格式为：IP:端口，即 nyc1.brookfree.pw:7000</strong>
    server_re = re.compile('(?<=即 ).*(?=</strong)')
    server = re.findall(server_re, page)
    logging.info(server)

    if not server:
        logging.error(u"获取Server信息失败！")
        sys.exit(0)

    pwd_re = re.compile('DOUBI.{10}')
    pwd = re.findall(pwd_re, page)
    # print("Server0(联通):%s\tServer1(电信):%s".decode('utf-8').encode(sys_type) % (server[0], server[1]))
    logging.info((server, pwd[0]))

    # 获取最低延的server
    # new_server = [s[0:s.index(":")] for s in server]
    # get_min_server(new_server)

    new_line = r"/Users/mac/he/soft/brook_darwin_amd64 client -l 127.0.0.1:1080 -i 127.0.0.1 -s %s -p %s" \
               % (server[int(carrier)], pwd[0])

    # 执行脚本
    os.system(new_line)
    logging.info(u"自动部署已完成")


if __name__ == '__main__':
    set_proxy()
