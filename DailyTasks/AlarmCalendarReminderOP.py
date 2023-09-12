from datetime import datetime, date, timedelta
from win32api import *
from win32gui import *
import win32con
import sys
import os
import time
from winotify import Notification

class DateOperations:

    def get_date(self, today_d=date.today()):
        if today_d != date.today():
            return date.today() + timedelta(today_d)
        else:
            return today_d

    @staticmethod
    def get_string_date(date_str):
        tarih = datetime.strptime(date_str, '%Y-%m-%d')
        turkish_months = {
            1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
            7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
        }
        turkish_days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        date_string = f"{tarih.day} {turkish_months[tarih.month]} {turkish_days[tarih.weekday()]}"

        return date_string

    def get_date_w_string(self, date_input):
        # date = date.strftime()
        return date_input.strftime("%B %d, %Y")


    def get_date_only_number(self, date_input):
        return date_input.split()[1].replace(",", "")

    @staticmethod
    def show_balloon(not_title, not_msg):
        cwd = os.getcwd()
        icon_path = os.path.join(cwd, "Niyetli.ico")
        toast = Notification(
            app_id="Niyetli",
            title=f"{not_title}",
            msg=f"{not_msg}",
            duration="long",
            icon=icon_path
        )
        return toast.show()

    @staticmethod
    def show_balloon2(self, title, msg):
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
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
        time.sleep(5)
        DestroyWindow(hwnd)


    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)
        return 0

    def get_date_info(self, date_str):
        date_format = "%Y-%m-%d"
        date_obj = datetime.strptime(date_str, date_format).date()
        today = date.today()
        diff = date_obj - today
        today_d = diff.days

        if today_d == 0:
            return "Bugün"
        elif today_d == -1:
            return "Dün"
        elif -7 <= today_d < -1:
            return "Geçen Hafta"
        elif date_obj.month == today.month and today_d < -7:
            return "Bu Ay"
        else:
            return "Geçen Ay"


# ----- Deneme Kod Alanı ------ #
# Buradaki kodları Niyetli.py' geçireceğim. Bu şekilde verilerde tarih düzenlemesini
#   düzgün bir şekilde gerçekleştirebilirim.
#
# do = DateOperations()
# datas = [["Not 1", "2023-07-01"], ["Not 1 ama uzun olan", "2023-07-01"], ["Not 2", "2023-07-11"], ["Not 3", "2023-07-17"]]
#
# temp_date = datas[0][1]
#
# for x in range(0, len(datas)):
#     title = do.get_date_info(datas[x][1])
#     if x == 0:
#         print(f"---{title}----")
#         print(f"----{datas[x][0]}----")
#
#     else:
#         if temp_date == datas[x][1]:
#             print(f"----{datas[x][0]}----")
#
#         else:
#             temp_Date = datas[x][1]
#             title = do.get_date_info(temp_Date)
#             print(f"---{title}----")
#             print(f"----{datas[x][0]}----")
#

# ----- Deneme Kod Alanı ------ #

# do = DateOperations()
# print(do.get_date("2023-06-30"))  # Geçen Ay
# print(do.get_date("2023-07-15"))  # Geçen Hafta
# print(do.get_date("2023-07-17"))  # Dün
# print(do.get_date("2023-07-18"))  # Bugün

# show_balloon("Niyetli'den mesaj var!", "Hatalar düzeltildi, Performans iyileştirmeleri yapıldı, Kedi videolarıyla kalpler eridi.")
# today = datetime.today()
# tomorrow = datetime.today()+timedelta(+1)
# print(datetime.now().strftime("%H:%M"))
# print(today.strftime("%A, %B %d, %Y"))
# print("Yarın:", tomorrow.strftime("%B %d, %Y"))
# print(get_date())
# print(get_date(-19))
# print(get_date_w_string(get_date(2)))
# print(get_date_only_number(get_date_w_string(get_date(3))))
