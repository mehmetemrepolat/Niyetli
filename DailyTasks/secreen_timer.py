from win32gui import GetWindowText, GetForegroundWindow
import time as t
import psutil
import win32process
from Niyetli.database.db_connector import Database
from datetime import time, date, datetime, timedelta
import datetime
import hashlib

db = Database()


Programs = []  # Çalışan program isimleri listesi
Times = []  # Çalışma sürelerini tutmak için liste
Day_Counter = []  # Günlük girilme sayısını tutmak için
ignored_programs = []  # Listede görüntülenmesine gerek görülmeyen programlar için. Kullanıcı isterse manuel ekleme yapabilecek.

class SecreenTimer:

    def md5_hash(self, program_name):
        md5_hash = hashlib.md5()
        md5_hash.update(program_name.encode('utf-8'))
        md5_digest = md5_hash.hexdigest()
        md5_program_name = md5_digest[0] + md5_digest[1] + md5_digest[2] + md5_digest[-1]
        return md5_program_name


    @staticmethod
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


    def get_App_index(self, app):
        return Programs.index(app) if app in Programs else -1


    def is_change_or_dont(self, before, after):
        if before == after:
            return False
        else:
            return True

    # X Günlük Y sayıda istatistiği verebilme
    # X sayıda istatistiği verebilme
    # Genel manada kullanıcının ekran süresi istatistiklerini verebilme
    #

    def get_all_statics(self):
        query = f"SELECT program_name, secreen_time, secreen_date, day_counter FROM secreen_timer"
        data = db.get_results(query)
        return data

    def get_statistics(self, number_of_stat=None, first_last_stat="ASC", days_stat=7):
        today = datetime.date.today()
        asked_date = today + timedelta(-days_stat)
        asked_date = asked_date.strftime("%Y-%m-%d")
        query = f"SELECT program_name, secreen_time, secreen_date, day_counter FROM secreen_timer WHERE secreen_date >= '{asked_date}'"
        if number_of_stat is not None:
            query += f" LIMIT {number_of_stat}"
        data = db.get_results(query)
        counts = {}
        for item in data:
            if item[0] in counts:
                counts[item[0]] += int(item[1])
            else:
                counts[item[0]] = int(item[1])

        result = []
        for item in data:
            found = False
            for r in result:
                if r['program_name'] == item[0]:
                    r['count'] += counts[item[0]]
                    r['time'] += int(item[3])
                    found = True
                    break
            if not found:
                result.append({
                    'program_name': item[0],
                    'count': counts[item[0]],
                    'time': int(item[3])
                })

        final_result = []
        for item in result:
            final_result.append([item['program_name'], item['count'], item['time']])

        return final_result


    def secreen_timer(self):
        fore_groundApp = ""
        temp_app = ""
        while True:
            if len(Programs) == 4:
                break
            while True:
                print("Program İsimleri:", Programs, " - Ekran Zamanı ", Times, " - Counter: ", Day_Counter)
                try:
                    if fore_groundApp == "":
                        fore_groundApp = self.get_ForeGroundApp()
                    if fore_groundApp not in Programs and fore_groundApp != "":
                        Programs.append(fore_groundApp)
                        Times.append(0)
                        Day_Counter.append(1)
                    else:
                        app_index = self.get_App_index(fore_groundApp)
                        Times[app_index] += 1
                        temp_app = fore_groundApp
                        t.sleep(1)
                        break
                except:
                    pass
            try:
                fore_groundApp = self.get_ForeGroundApp()
                if self.is_change_or_dont(temp_app, fore_groundApp):
                    Day_Counter[self.get_App_index(fore_groundApp)] += 1
            except:
                pass
        for x in range(0, len(Programs)):
            program_id = self.md5_hash(Programs[x])
            db.timer_into_database(program_id, Programs[x], '1', Times[x], Day_Counter[x])



sc = SecreenTimer()
print(sc.get_all_statics())
# secreen_timer()
# print(get_statistics(100, "ASC", 100))
# list = get_statistics2(100, "ASC", 100)



# print(list)

# print("---")
# print(list[0])
