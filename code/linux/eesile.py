import os
import json
import subprocess
import requests
from bs4 import BeautifulSoup


class Eesile(object):
    def __init__(self):
        requests.packages.urllib3.disable_warnings()
        self.cookie_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookie")
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        self.base_uri = ''
        self.redirect_uri = ''

    def login(self):
        if not os.path.exists(self.cookie_file):
            open(self.cookie_file, 'w+')
        with open(self.cookie_file, 'r') as f:
            if os.path.getsize(self.cookie_file):
                self.session.cookies = requests.utils.cookiejar_from_dict(json.load(f))
        self.redirect_uri = 'https://eesile.org/user/ticket'
        login_test = self.session.get(self.redirect_uri, verify=False).content.decode('utf-8')
        if '工单' in login_test:
            print('成功读取Cookie！')
            return True
        else:
            print('重新登录！')
            self.base_uri = 'https://eesile.org/auth/login'
            data = {
                'email': '545589629@qq.com',
                'passwd': 'heyongman',
                'code': ''
            }
            response = self.session.post(self.base_uri, data=data, verify=False)
            data = response.content.decode('unicode-escape')
            if '欢迎回来' in data:
                self.redirect_uri = 'https://eesile.org/user'
                response = self.session.get(self.redirect_uri, verify=False)
                if '用户中心' in response.content.decode('utf-8'):
                    cookie = requests.utils.dict_from_cookiejar(self.session.cookies)
                    with open(self.cookie_file, 'w') as f:
                        json.dump(cookie, f)
                    return True
            else:
                return False

    def get_server(self):
        # 免费_俄1_电信:313,免费_日1:357,免费_美国:358
        # self.redirect_uri = 'https://eesile.org/user/node'
        # response = self.session.get(self.redirect_uri, verify=False)
        # html = response.content.decode('utf-8')
        a = {}
        for node in [313, 357, 358]:
            self.redirect_uri = 'https://eesile.org/user/node/%s?ismu=443&relay_rule=0' % node
            response = self.session.get(self.redirect_uri, verify=False)
            res = response.content.decode('utf-8')
            soup = BeautifulSoup(res, 'html.parser')
            server = json.loads(soup.textarea.string)
            server_ip = server['server']
            # print(server_ip)
            p = subprocess.Popen("ping -W 1000 -c 1 %s | awk -F '[ =]' '{print $10}'" % server_ip, stdout=subprocess.PIPE, shell=True)
            delay = p.stdout.readlines()[1].decode('utf-8')[:-2]
            # print('delay:', delay)
            if delay.strip() != '' and eval(delay) <= 1000:
                a[server_ip] = (server, eval(delay))
        b = sorted(a.items(), key=lambda x: x[1][1])
        return b

    def main(self):
        if not self.login():
            print('登录失败')
        else:
            print("登录成功！")
            server = self.get_server()
            print(server)
            with open(self.config_file, 'w+') as f:
                json.dump(server[0][1][0], f)


if __name__ == '__main__':
    eesile = Eesile()
    eesile.main()
