from win32api import *
from win32gui import *
import win32con
import sys, os
import struct
import time


class WindowsBalloonTip:
    classAtom = None

    def __init__(self, *args, **kwargs):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }

        # Register the Window class.
        self.hinst = GetModuleHandle(None)
        if not WindowsBalloonTip.classAtom:
            wc = WNDCLASS()
            wc.hInstance =  self.hinst
            wc.lpszClassName = "PythonTaskbar"
            wc.lpfnWndProc = message_map # could also specify a wndproc.
            WindowsBalloonTip.classAtom = RegisterClass(wc)


        iconPathName = os.path.abspath(os.path.join( sys.path[0], kwargs.get("icon", "balloontip.ico") ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           self.hicon = LoadImage(self.hinst, iconPathName,   win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
           self.hicon = LoadIcon(0, win32con.IDI_APPLICATION)

    def show(self,title, msg, duration=10):
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( WindowsBalloonTip.classAtom, "Taskbar", style,  0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,  0, 0, self.hinst, None)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,  self.hicon, "Balloon  tooltip",title,200,msg))
        time.sleep(duration)
        Shell_NotifyIcon(NIM_DELETE, nid)
        ShowWindow(self.hwnd, win32con.SW_HIDE)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)