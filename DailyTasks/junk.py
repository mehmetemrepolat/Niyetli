from datetime import datetime, date, timedelta
from win32api import *
from win32gui import *
import win32con
import sys
import os
import struct
import time
import threading


def get_date(today = date.today()):
    if today != date.today():
        return date.today() + timedelta(today)
    else:
        return today


def get_date_w_string(date):
    # date = date.strftime()
    return date.strftime("%B %d, %Y")


def get_date_only_number(date):
    return date.split()[1].replace(",", "")


def show_balloon(title, msg):
    message_map = {
        win32con.WM_DESTROY: OnDestroy,
    }
    wc = WNDCLASS()
    hinst = wc.hInstance = GetModuleHandle(None)
    wc.lpszClassName = "PythonTaskbar"
    wc.lpfnWndProc = message_map
    classAtom = RegisterClass(wc)
    style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
    hwnd = CreateWindow(classAtom, "Taskbar", style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, hinst, None)
    UpdateWindow(hwnd)
    iconPathName = os.path.abspath(os.path.join(sys.path[0], "Niyetli.ico"))
    icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
    try:
        hicon = LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
    except:
        hicon = LoadIcon(0, win32con.IDI_APPLICATION)

    flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
    nid = (hwnd, 0, flags, win32con.WM_USER + 20, hicon, "tooltip")
    Shell_NotifyIcon(NIM_ADD, nid)
    Shell_NotifyIcon(NIM_MODIFY, (hwnd, 0, NIF_INFO, win32con.WM_USER + 20, hicon, "Balloon  tooltip", msg, 200, title))

    time.sleep(10)
    DestroyWindow(hwnd)


def OnDestroy(hwnd, msg, wparam, lparam):
    nid = (hwnd, 0)
    Shell_NotifyIcon(NIM_DELETE, nid)
    PostQuitMessage(0)


def schedule_task(title, msg, year, month, day, hour, minute):
    schedule_time = datetime(year, month, day, hour, minute)
    while datetime.now() < schedule_time:
        time.sleep(1)

    show_balloon(title, msg)


def run_in_background():
    schedule_task("Niyetli'den mesaj var!", "Merhabalar", 2023, 3, 10, 22, 10)
    while True:
        # Metodun içeriği burada olacak
        time.sleep(10)  # 10 saniye bekle



run_in_background()
# thread = threading.Thread(target=run_in_background)
# thread.daemon = False  # !Ana program kapatıldığında thread de sonlandırılır
# thread.start()
# !Reminder da hata var düzeltilmesi gerekiyor.
