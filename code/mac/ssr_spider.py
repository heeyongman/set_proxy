#!/usr/bin/env python3
import os
import re
import ping3
import base64

curr_path = os.path.dirname(os.path.abspath(__file__))


def get_ssrs():
    with open('/Users/he/Documents/ssr') as f:
        s = f.read()
        f.close()
    ssr_reg = r'ssr://(\w{10,})'
    ssrs = re.findall(ssr_reg, s)
    ssrs = list(set(ssrs))
    print('已获取到ssr，数量：%s' % len(ssrs))
    get_delay(ssrs)


def get_delay(ssrs):
    # 获取低延迟的账号
    ssr_delay_ser = []
    for ssr in ssrs:
        ssr_fill = ssr.replace('_', '/').replace('-', '+')
        missing_padding = 4 - len(ssr_fill) % 4
        if missing_padding:
            ssr_fill += '=' * missing_padding
        # print(ssr_fill)
        try:
            ssr_decode = base64.b64decode(ssr_fill).decode('utf-8')
        except:
            ssrs.remove(ssr)
            continue
        ip = ssr_decode.split(':')[0]
        d = ping3.ping(ip, 0.5)
        if not d:
            continue
        ssr_delay_ser.append((ip, d, ssr_decode))
        ssr_delay_ser.sort(key=lambda tup: tup[1], reverse=False)

    # 获取低延迟的账号
    ssr_delay_ser = ssr_delay_ser[0:10]
    parse_ssr(ssr_delay_ser)


# 将账号解析出来
def parse_ssr(ssr_delay_ser):
    ssr_list = []
    ssr_final = {}
    for ssr in ssr_delay_ser:
        ssr_split = ssr[2].split(':')
        # 解析密码
        pwd_origin = ssr_split[5].split('/')[0]
        missing_padding = 4 - len(pwd_origin) % 4
        if missing_padding:
            pwd_origin += '=' * missing_padding
        pwd = base64.b64decode(pwd_origin).decode('utf-8')

        # 组建json
        # server,server_port,protocol,method,obfs,password
        print(ssr_split)
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
    # save_ssr_json(ssr_final)


# print(ssr_final)
# 将账号信息保存为json文件
def save_ssr_json(ssr_final):
    with open(curr_path + os.sep + 'ssr_config.json', mode='w') as f:
        f.write(str(ssr_final).replace('\'', '\"'))
        f.close()
    print('写入文件成功')


if __name__ == '__main__':
    get_ssrs()
