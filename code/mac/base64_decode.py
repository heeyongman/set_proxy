#!/usr/bin/env python3
import base64
import ping3
import re
import os
import json

# f = ping3.ping(e, 1)
# print(f)

with open('/Users/he/Downloads/ssr.txt') as f:
    s = f.read()
    f.close()

r = r'ssr://(.*)'
res = re.findall(r, s)
for ssr in res:
    ssr_fill = ssr.replace('_', '/').replace('-', '+')
    missing_padding = 4 - len(ssr_fill) % 4
    if missing_padding:
        ssr_fill += '=' * missing_padding
    ssr_decode = base64.b64decode(ssr_fill).decode('utf-8')
    # ip = ssr_decode.split(':')[0]
    # delay = ping3.ping(ip, 1)
    # print(ssr_decode)
    ssr_split = ssr_decode.split(':')
    delay = ping3.ping(ssr_split[0])
    d = 1 if not delay else delay


ssr_list = []
ssr_final = {}
for ssr in res:
    ssr_fill = ssr.replace('_', '/').replace('-', '+')
    missing_padding = 4 - len(ssr_fill) % 4
    if missing_padding:
        ssr_fill += '=' * missing_padding
    ssr_decode = base64.b64decode(ssr_fill).decode('utf-8')
    # ip = ssr_decode.split(':')[0]
    # delay = ping3.ping(ip, 1)
    # print(ssr_decode)
    ssr_split = ssr_decode.split(':')
    pwd_origin = ssr_split[5].split('/')[0]
    missing_padding = 4 - len(pwd_origin) % 4
    if missing_padding:
        pwd_origin += '=' * missing_padding
    pwd = base64.b64decode(pwd_origin).decode('utf-8')
    # print(ssr_split)
    # server,server_port,protocol,method,obfs,password
    ssr_json = {
        "remarks": ssr_split[0],
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
    ssr_list.append(ssr_json)
    ssr_final = {
        "configs": ssr_list
    }

# print(ssr_final)
with open(curr_path + os.sep + 'ssr_config.json', mode='w') as f:
    f.write(str(ssr_final).replace('\'', '\"'))
    f.close()



