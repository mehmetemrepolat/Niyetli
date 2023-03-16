import win32gui
import win32api
import win32con
import win32process
import time
import keyboard
import pyautogui


sleep_time = 1


def change_window(repeat=1):
    if repeat == 1:
        time.sleep(sleep_time)
        pyautogui.hotkey('alt', 'tab')
    else:
        # "ctrl" tuşuna basılı tut
        pyautogui.keyDown('alt')
        for x in range(0, repeat):
            time.sleep(sleep_time)
            pyautogui.press('tab')
            time.sleep(10)
        # "ctrl" tuşunu serbest bırak
        pyautogui.keyUp('alt')


# Aktif pencerenin adını almak için fonksiyon

def get_active_window_title():
    window = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(window)
    handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
    process_name = win32process.GetModuleFileNameEx(handle, 0)
    return process_name.split("\\")[-1]


# Son pencere adını saklamak için bir değişken oluştur
def check_active_window_for_opera():
    last_window_title = ""
    while True:
        # 1 saniye bekle
        time.sleep(1)
        # Aktif pencerenin adını al
        active_window_title = get_active_window_title()
        # Aktif pencerenin adını ekrana yazdır, ancak son pencere adından farklıysa
        if active_window_title != last_window_title:
            print(active_window_title)
            # Eğer aktif program Opera ise
            if "opera" in active_window_title.lower():
                # Boşluk tuşuna basıldıysa
                if keyboard.is_pressed(" "):
                    # Burada yapmak istediğiniz işlemi gerçekleştirin
                    pass
            # Son pencere adını güncelle
            last_window_title = active_window_title


# get_active_window_title()
# check_active_window_for_opera()
# change_window()
