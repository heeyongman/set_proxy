# coding:utf-8

import ctypes.wintypes

if __name__ == "__main__":
    import os, sys

    current_path = os.path.dirname(os.path.abspath(__file__))
    python_path = os.path.abspath(os.path.join(current_path, os.pardir, 'python27', '1.0'))
    noarch_lib = os.path.abspath(os.path.join(python_path, 'lib', 'noarch'))
    sys.path.append(noarch_lib)
    win32_lib = os.path.abspath(os.path.join(python_path, 'lib', 'win32'))
    sys.path.append(win32_lib)

import ctypes
import os
import webbrowser

import _winreg as winreg
import win32_proxy_manager

# import config
# import module_init
# import update

from systray import SysTrayIcon, win32_adapter

import locale

lang_code, code_page = locale.getdefaultlocale()

import logging
import traceback

current_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.abspath(os.path.join(current_path, os.pardir, os.pardir, os.pardir))

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.FileHandler(filename=log_path+'\\get_proxy.log', encoding='utf-8')
logging.basicConfig(filename=log_path + '\\get_proxy.log', level=logging.DEBUG, format=LOG_FORMAT)


class Win_tray:
    def __init__(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon", "favicon.ico")
        self.systray = SysTrayIcon(icon_path, "XX-Net", self.make_menu(), self.on_quit, left_click=self.on_show,
                                   right_click=self.on_right_click)

        reg_path = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
        self.INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)

        # proxy_setting = config.get(["modules", "launcher", "proxy"], "smart_router")
        # if proxy_setting == "pac":
        #     self.on_enable_pac()
        # elif proxy_setting == "gae":
        #     self.on_enable_gae_proxy()
        # elif proxy_setting == "x_tunnel":
        #     self.on_enable_x_tunnel()
        # elif proxy_setting == "smart_router":
        #     self.on_enable_smart_router()
        # elif proxy_setting == "disable":
        #     # Don't disable proxy setting, just do nothing.
        #     pass
        # else:
        #     xlog.warn("proxy_setting:%r", proxy_setting)

    def get_proxy_state(self):
        try:
            AutoConfigURL, reg_type = winreg.QueryValueEx(self.INTERNET_SETTINGS, 'AutoConfigURL')
            if AutoConfigURL:
                if AutoConfigURL == "https://www.txthinking.com/pac/white.pac":
                    return "pac"
                else:
                    return "unknown"
        except:
            pass

        try:
            ProxyEnable, reg_type = winreg.QueryValueEx(self.INTERNET_SETTINGS, 'ProxyEnable')
            if ProxyEnable:
                ProxyServer, reg_type = winreg.QueryValueEx(self.INTERNET_SETTINGS, 'ProxyServer')
                if ProxyServer == "127.0.0.1:8087":
                    return "gae"
                if ProxyServer == "127.0.0.1:1080":
                    return "Socks5"
                else:
                    return "unknown"
        except:
            pass

        return "disable"

    def on_right_click(self):
        self.systray.update(menu=self.make_menu())
        self.systray._show_menu()

    def make_menu(self):
        global menu_options
        proxy_stat = self.get_proxy_state()
        proxy_checked = win32_adapter.fState.MFS_CHECKED if proxy_stat == "disable" else 0
        pac_checked = win32_adapter.fState.MFS_CHECKED if proxy_stat == "pac" else 0
        # x_tunnel_checked = win32_adapter.fState.MFS_CHECKED if proxy_stat == "x_tunnel" else 0
        # smart_router_checked = win32_adapter.fState.MFS_CHECKED if proxy_stat == "smart_router" else 0
        # pac_checked = win32_adapter.fState.MFS_CHECKED if proxy_stat == "pac" else 0
        # disable_checked = win32_adapter.fState.MFS_CHECKED if proxy_stat == "disable" else 0

        if lang_code == "zh_CN":
            menu_options = [(u"设置(待完善)", None, self.on_show, 0)]
            # if config.get(["modules", "gae_proxy", "auto_start"], 0) == 1:
            # menu_options.append((u"全局通过GAEProxy代理", None, self.on_enable_gae_proxy, win32_adapter.fState.MFS_CHECKED))

            # if config.get(["modules", "x_tunnel", "auto_start"], 0) == 1:
            # menu_options.append((u"全局通过X-Tunnel代理", None, self.on_enable_x_tunnel, 0))

            # if config.get(["modules", "smart_router", "auto_start"], 0) == 1:
            # menu_options.append((u"全局通过智能路由代理", None, self.on_enable_smart_router, win32_adapter.fState.MFS_CHECKED))

            menu_options += [
                (u"全局PAC智能代理", None, self.on_enable_pac, pac_checked),
                (u"取消全局代理", None, self.on_disable_proxy, proxy_checked),
                (u'退出', None, SysTrayIcon.QUIT, False)]

        return tuple(menu_options)

    def on_show(self, widget=None, data=None):
        self.show_control_web()

    def on_enable_gae_proxy(self, widget=None, data=None):
        win32_proxy_manager.set_proxy("127.0.0.1:8087")

    def on_enable_pac(self, widget=None, data=None):
        curr_path = os.path.dirname(os.path.abspath(__file__))
        try:
            cmd = curr_path + r"\\brook_windows_386.exe systemproxy -u https://www.txthinking.com/pac/white.pac"
            os.system(cmd)
        except Exception:
            logging.error('on_enable_pac:%s' % traceback.format_exc())
        # win32_proxy_manager.set_proxy("https://www.txthinking.com/pac/white.pac")
        # config.set(["modules", "launcher", "proxy"], "pac")
        # config.save()

    def on_disable_proxy(self, widget=None, data=None):
        curr_path = os.path.dirname(os.path.abspath(__file__))
        try:
            cmd = curr_path + r"\\brook_windows_386.exe systemproxy -r"
            os.system(cmd)
        except Exception:
            logging.error("on_disable_proxy:%s" % traceback.format_exc())
        # win32_proxy_manager.set_proxy("")
        # win32_proxy_manager.disable_proxy()
        # config.set(["modules", "launcher", "proxy"], "disable")
        # config.save()

    def show_control_web(self, widget=None, data=None):
        # host_port = config.get(["modules", "launcher", "control_port"], 8085)
        host_port = 8085
        webbrowser.open("http://127.0.0.1:%s/" % host_port)
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    def on_quit(self, widget, data=None):
        # proxy_setting = config.get(["modules", "launcher", "proxy"], "disable")
        # if proxy_setting != "disable":
        #     win32_proxy_manager.disable_proxy()
        # module_init.stop_all()
        cmd = 'taskkill /F /IM brook_windows_386.exe'
        os.system(cmd)
        nid = win32_adapter.NotifyData(self.systray._hwnd, 0)
        win32_adapter.Shell_NotifyIcon(2, ctypes.byref(nid))
        os._exit(0)

    def serve_forever(self):
        logging.info("\n\n[step3]:enter win_tray")
        self.systray._message_loop_func()

    def dialog_yes_no(self, msg="msg", title="Title", data=None, callback=None):
        res = ctypes.windll.user32.MessageBoxW(None, msg, title, 1)
        # Yes:1 No:2
        if callback:
            callback(data, res)
        return res


sys_tray = Win_tray()


def main():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    sys_tray.serve_forever()


if __name__ == '__main__':
    main()
