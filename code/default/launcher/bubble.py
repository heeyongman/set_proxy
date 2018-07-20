# -*- encoding:utf-8 -*-
##############################
#
# 程序名:python桌面托盘气泡
# 文件名:bubble.py
# 功能 :实现桌面托盘气泡提示功能
# modify:by heyongman 2018.7.18
# program:python2.7
# 适用  :windowsXP -windows10
#
##############################
import sys
import os
import struct
import time
import win32con

from win32api import *

# Try and use XP features, so we get alpha-blending etc.
try:
    from winxpgui import *
except ImportError:
    from win32gui import *

curr_path = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(curr_path, "icon", "favicon.ico")


class MainWindow:
    def __init__(self):
        # 初始化变量
        self.title = ""
        self.msg = ""
        self.duration = 5  # 延时5秒
        self.hwnd = None
        self.hinst = None
        self.regOk = False
        # self.creWind()

    def creWind(self):
        # Register the Window class.
        wc = WNDCLASS()
        self.hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbarDemo"  # 字符串只要有值即可,下面3处也一样
        wc.lpfnWndProc = {win32con.WM_DESTROY: self.OnDestroy}  # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow(classAtom, "Taskbar Demo", style,
                                 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                 0, 0, self.hinst, None
                                 )
        UpdateWindow(self.hwnd)

    # start bubble
    def startBubble(self, title, msg, duration=3, close=True):

        if (self.hwnd == None):
            self.creWind()
        self.title = title
        self.msg = msg
        self.duration = duration

        iconPathName = os.path.abspath(os.path.join(curr_path, "icon", "favicon.ico"))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = LoadImage(self.hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "Balloon  tooltip demo")
        try:
            Shell_NotifyIcon(NIM_ADD, nid)
        except:
            pass
            # self.hwnd == None

        # self.show_balloon(self.title, self.msg)
        # nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "tooltip")
        # Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY,
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER + 20,
                          hicon, "Balloon  tooltip", msg, 200, title))
        if close:
            time.sleep(self.duration)
            # ReleaseDC(self.hwnd,wc)
            # DeleteDC(wc)
            try:
                DestroyWindow(self.hwnd)
                # self.hwnd == None
            except:
                return None

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)  # Terminate the app.


bubble = MainWindow()

if __name__ == '__main__':
    msgTitle = u"您有一条短消息"
    msgContent = "hello python"
    # msgTitle = msgTitle
    bubble = MainWindow()
    bubble.startBubble(msgTitle, msgContent)
