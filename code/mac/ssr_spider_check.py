#!/usr/bin/env python3
import threading
from app.ss import crawler, ssr_check
import requests
import ping3
import re
import json
import base64
import os
import urllib3
import copy

curr_path = os.path.dirname(os.path.abspath(__file__))
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 禁止不安全警告


def get_ssrs():
    ssr_list = []
    url_list = ['https://raw.githubusercontent.com/AmazingDM/sub/master/ssrshare.com',
                'https://lisuanlaoji.link/sub/HyFvwKMP7YsD7gQF']
    # 获取文件的数据
    with open('/Users/he/Documents/ssr') as f:
        ssr_file = f.read()
        f.close()
    if len(ssr_file) > 0:
        ssr_reg = r'ssr://(\w{10,})'
        str_ssr = re.findall(ssr_reg, ssr_file)
        ssr_list.append(str_ssr)
        print('文件数据读取完毕')
    else:
        print('忽略文件数据')

    # 抓取网站的数据
    for u in url_list:
        res = requests.get(u)
        if res.ok:
            ssr_decode = base64.b64decode(res.text).decode('utf-8')
            ssr_reg = r'ssr://(\w{10,})'
            str_ssrs = re.findall(ssr_reg, ssr_decode)
            ssr_list.extend(str_ssrs)
            print('当前网站抓取完毕：%s' % u)
        else:
            print('当前网站抓取失败：%s' % u)

    return ssr_list


def validate_ssrs(ssrs):
    list_str_ssr = list(set(ssrs))
    print('已读取到ssr，数量：%s' % len(list_str_ssr))

    # 解析账号
    ssr_list = []
    for str_ssr in list_str_ssr:
        ssr_fill = str_ssr.replace('_', '/').replace('-', '+')
        missing_padding = 4 - len(ssr_fill) % 4
        if missing_padding:
            ssr_fill += '=' * missing_padding
        try:
            ssr_decode = base64.b64decode(ssr_fill).decode('utf-8')
        except:
            list_str_ssr.remove(str_ssr)
            continue
        # 解析密码
        ssr_split = ssr_decode.split(':')
        str_end = ssr_split[5].replace('_', '/').replace('-', '+')
        pwd_origin = str_end.split('/')[0]
        missing_padding = 4 - len(pwd_origin) % 4
        if missing_padding:
            pwd_origin += '=' * missing_padding
        pwd = base64.b64decode(pwd_origin).decode('utf-8')
        # 解析后缀
        params = str_end.split('/?')[1]
        dic = dict([item.split('=') for item in params.split('&')])
        for k, v in dic.items():
            val = v
            missing_padding = 4 - len(v) % 4
            if missing_padding:
                val += '=' * missing_padding
            dic[k] = base64.b64decode(val).decode('utf-8')
        # 构建json
        # server,server_port,protocol,method,obfs,password
        # print(ssr_split)
        ssr_json = {
            # "remarks": ssr_split[0],
            "server": ssr_split[0],
            "server_port": int(ssr_split[1]),
            "method": ssr_split[3],
            "obfs": ssr_split[4],  # 混淆
            # "obfsparam": "",
            "password": pwd,
            # "tcp_over_udp": False,
            # "udp_over_tcp": False,
            "protocol": ssr_split[2],  # 协议
            # "obfs_udp": False,
            # "enable": True
        }
        ssr_json.update(dic)
        ssr_list.append(ssr_json)

    # 获取低延迟的账号
    low_delay_servers = []
    for ssr in ssr_list:
        ip = ssr['server']
        d = None
        try:
            d = ping3.ping(ip, 0.5)
        except Exception as e:
            print(e)
        if d:
            low_delay_servers.append(ssr)
    # ssr_list.sort(key=lambda tup: tup[1], reverse=False)
    print('去除高延迟账号后剩余个数：%s' % len(low_delay_servers))
    return low_delay_servers


def save_ssr_json(ser):
    with open(curr_path + os.sep + 'ssr_config.json', mode='w') as f:
        f.write(str(ser).replace('\'', '\"'))
        f.close()
    print('写入文件成功')


if __name__ == '__main__':
    server = {
        "server": "192.54.56.21",
        "server_port": 10292,
        "password": "lmJK2X",
        "method": "aes-256-cfb",
    }
    ser_list = get_ssrs()
    low_delay_servers = validate_ssrs(ser_list)
    print('开始验证账号可用性...')
    available_servers = []
    for server in low_delay_servers:
        dic = copy.deepcopy(server)
        result, info, speed_download = ssr_check.test_socks_server(dictionary=dic)
        print('测试结果：', result, info[:-2], speed_download)
        server['speed_download'] = speed_download
        if result:
            available_servers.append(server)
    print('去除不可用账号后剩余个数：%s' % len(available_servers))
    # 根据速度排序
    available_servers.sort(key=lambda d: d['speed_download'], reverse=False)
    available_servers = available_servers[:3]
    for server in available_servers:
        server.pop('speed_download')
    ssr_final = {"configs": available_servers}
    save_ssr_json(ssr_final)
