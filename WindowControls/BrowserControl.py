import time
import pyautogui

sleep_time = 1


def new_tab():
    time.sleep(sleep_time)
    pyautogui.hotkey('ctrl', 't')


def close_tab():
    time.sleep(sleep_time)
    pyautogui.hotkey('ctrl', 'w')


def change_tab(repeat = 1):
    if repeat == 1:
        time.sleep(sleep_time)
        pyautogui.hotkey('ctrl', 'tab')
    else:
        # "ctrl" tuşuna basılı tut
        pyautogui.keyDown('ctrl')

        for x in range(0, repeat):
            time.sleep(sleep_time)
            pyautogui.press('tab')

        # "ctrl" tuşunu serbest bırak
        pyautogui.keyUp('ctrl')


def go_to_url(url):
    time.sleep(sleep_time)
    pyautogui.hotkey('ctrl', 't')
    time.sleep(sleep_time)
    pyautogui.typewrite(url)
    pyautogui.press('enter')


def text_search(text):
    time.sleep(sleep_time)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(sleep_time)
    pyautogui.typewrite(text)
    time.sleep(sleep_time)
    pyautogui.press('enter')


def go_back():
    time.sleep(sleep_time)
    pyautogui.hotkey('alt', 'left')


def go_forward():
    time.sleep(sleep_time)
    pyautogui.hotkey('alt', 'right')


# Scroll down işlemini gerçekleştirir
def scroll_UpDown(pixels):
    pyautogui.scroll(pixels, x=0, y=0)


# time.sleep(3)
# scroll_UpDown(100)
# go_to_url("youtube.com")
# go_back()
# go_forward()
# new_tab()
# close_tab()
# text_search("Niyetli")
# change_window(3)
# change_tab(3)


