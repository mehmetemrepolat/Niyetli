from win32gui import GetWindowText, GetForegroundWindow
import time as t
import psutil
import win32process
from Niyetli.database.db_connector import Database
from datetime import time, date, datetime
import hashlib

db = Database()


Programs = []  # Çalışan program isimleri listesi
Times = []  # Çalışma sürelerini tutmak için liste
Day_Counter = []  # Günlük girilme sayısını tutmak için
ignored_programs = []  # Listede görüntülenmesine gerek görülmeyen programlar için. Kullanıcı isterse manuel ekleme yapabilecek.


def md5_hash(program_name):
    md5_hash = hashlib.md5()
    md5_hash.update(program_name.encode('utf-8'))
    md5_digest = md5_hash.hexdigest()
    md5_program_name = md5_digest[0] + md5_digest[1] + md5_digest[2] + md5_digest[-1]
    return md5_program_name


def get_ForeGroundApp():
    if psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "") == 'explorer':
        hwnd = GetForegroundWindow()
        title = GetWindowText(hwnd)
        return title

    else:
        hwnd = GetForegroundWindow()
        title = GetWindowText(hwnd)
        # return title
        return psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")


def get_App_index(app):
    return Programs.index(app) if app in Programs else -1


def is_change_or_dont(before, after):
    if before == after:
        return False
    else:
        return True


def secreen_timer():
    fore_groundApp = ""
    temp_app = ""
    while True:
        if len(Programs) == 4:
            break
        while True:
            print("Program İsimleri:", Programs, " - Ekran Zamanı ", Times, " - Counter: ", Day_Counter)
            try:
                if fore_groundApp == "":
                    fore_groundApp = get_ForeGroundApp()
                if fore_groundApp not in Programs and fore_groundApp != "":
                    Programs.append(fore_groundApp)
                    Times.append(0)
                    Day_Counter.append(1)
                else:
                    app_index = get_App_index(fore_groundApp)
                    Times[app_index] += 1
                    temp_app = fore_groundApp
                    t.sleep(1)
                    break
            except:
                pass
        try:
            fore_groundApp = get_ForeGroundApp()
            if is_change_or_dont(temp_app, fore_groundApp):
                Day_Counter[get_App_index(fore_groundApp)] += 1
        except:
            pass
    for x in range(0, len(Programs)):
        program_id = md5_hash(Programs[x])
        db.timer_into_database(program_id, Programs[x], '1', Times[x], Day_Counter[x])


# secreen_timer()
