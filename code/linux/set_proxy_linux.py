#!/usr/bin/python3
import os
import sys
import re
import logging
import traceback

try:
    import requests
except:
    os.system("sudo pip install requests")
    import requests

try:
    import ping3
except:
    os.system("sudo pip install ping3")
    import ping3

sys_type = sys.getfilesystemencoding()

# 判断数据文件是否存在
curr_path = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(curr_path, "data")
log_path = os.path.join(curr_path, "set_proxy.log")
status = os.path.exists(data_file_path)
sys.path.append(curr_path)
carrier = "0"  # min_delay_server

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
# logging.FileHandler(filename=log_path+'\\get_proxy.log', encoding='utf-8')
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=LOG_FORMAT)


def bubble(title, content):
    cmd = "notify-send '%s' '%s'" % (title, content)
    os.system(cmd)


def get_page(url):
    try:
        res = requests.get(url).text
        return res
    except Exception:
        logging.error(traceback.format_exc())
        bubble('GetProxy', '连接服务器异常，请保持网络畅通')
        sys.exit(0)


def modify_hosts():
    os.system('echo -e "\n104.28.2.6 doub.io\n"|sudo tee -a /etc/hosts')
    logging.info("hosts修改成功")


def get_min_server(server):
    # get min_delay_server
    delay = []
    for s in server:
        resp = os.popen("ping -c 1 %s|grep time=" % s).readlines()
        server_re = re.compile('(?<=time=).*?(?= ms)')
        o = re.findall(server_re, str(resp))
        print(o)
        if o:
            delay.append(eval(o[0]))
    if not delay:
        bubble("GetProxy", "服务器异常.")
    min_server = delay.index(min(delay))
    logging.info("min_server_num: %s" % min_server)
    logging.info("min_server: %s" % server[int(min_server)])
    return min_server


def set_proxy():
    modify_hosts()
    logging.info("获取Server中...")
    bubble('GetProxy', '获取连接')
    ser_url = "https://doub.io/sszhfx/"
    page = get_page(ser_url)

    # <strong>服务器栏的格式为：IP:端口，即 nyc1.brookfree.pw:7000</strong>
    server_re = re.compile('(?<=即 ).*(?=</strong)')
    server = re.findall(server_re, page)
    logging.info(server)

    if not server:
        logging.error("获取Server信息失败！")
        bubble('GetProxy', '获取Server失败，请保持网络畅通')
        sys.exit(0)

    pwd_re = re.compile('DOUBI.{10}')
    pwd = re.findall(pwd_re, page)
    # print("Server0(联通):%s\tServer1(电信):%s".decode('utf-8').encode(sys_type) % (server[0], server[1]))
    logging.info((server, pwd[0]))

    # 获取最低延的server
    new_server = [s[0:s.index(":")] for s in server]
    server_index = get_min_server(new_server)

    bubble('GetProxy', '自动部署已完成，Enjoy! :)')
    logging.info("自动部署已完成")
    cmd = "./brook client -l 127.0.0.1:1080 -i 127.0.0.1 -s %s -p %s" % (server[server_index], pwd[0])
    os.system(cmd)
    os.system("pwd")
    logging.info("程序已关闭")

if __name__ == '__main__':
    set_proxy()
