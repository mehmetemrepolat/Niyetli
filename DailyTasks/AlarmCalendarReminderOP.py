import threading
from datetime import datetime, date, timedelta
from win32api import *
from win32gui import *
import win32con
import sys
import os
import time
from winotify import Notification
import pygame
from playsound import playsound
import mutagen

class DateOperations:

    # 2023-11-13
    def get_date(self, today_d=date.today()):
        if today_d != date.today():
            return date.today() + timedelta(today_d)
        else:
            return today_d

    # 13 Kasım Pazartesi

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

class AlarmAndNotificationOperations:


    def play_sound(self, path, mode):
        def get_voice_duration(title):
            audio = mutagen.File(title)
            duration_s = audio.info.length
            return int(duration_s) + 1

        try:
            def play_thread():
                pygame.mixer.init()
                pygame.mixer.music.load(path)
                if mode == 'alarm':
                    pygame.mixer.music.play(loops=-1)
                    time.sleep(30)
                    pygame.mixer.music.stop()
                    pygame.quit()
                elif mode == 'notification':
                    pygame.mixer.music.play()
                    time.sleep(get_voice_duration(path))
                    pygame.mixer.music.stop()
                    pygame.quit()

            thread = threading.Thread(target=play_thread)
            thread.start()

        except Exception as e:
            print("AlarmAndNotificationOperations.play_sound Error")


    def show_balloon(self, not_title, not_msg, mode = 'notification'):
        # Ayrı bir veritabanı bağlantısı gerekebilir.
        # Kullanıcının kendi localinde bulunan bir veritabanı bağlantısı.
        # Veya veritabanı yerine bilgilerin tutulacağı bir dosya gerekebilir.

        if mode == 'notification':
            duration = "short"
            sound_path = "sounds/notification2.wav"  # Bunu veritabanından çekebilir hale gelmemiz gerekiyor.
            self.play_notification_sound = threading.Thread(target=self.play_sound, args=(sound_path, mode))
            self.play_notification_sound.start()

        elif mode == 'alarm':
            duration = "long"
            sound_path = "sounds/alarm1.wav"
            for x in range(0, 5):
                self.play_notification_sound = threading.Thread(target=self.play_sound, args=(sound_path, mode))
                self.play_notification_sound.start()


        else:
            print("Hata! AlarmAndNotificationOperations")


        cwd = os.getcwd()
        icon_path = os.path.join(cwd, "Niyetli.ico")
        toast = Notification(
            app_id="Niyetli",
            title=f"{not_title}",
            msg=f"{not_msg}",
            duration=duration,
            icon=icon_path
        )
        return toast.show()




# ano = AlarmAndNotificationOperations()
# ano.show_balloon("Deneme", "Deneme mesajı", "notification")

# play_sound('sounds/notification2.wav')

# ----- Deneme Kod Alanı ------ #



# today = datetime.today()
# tomorrow = datetime.today()+timedelta(+1)
# print(datetime.now().strftime("%H:%M"))
# print(today.strftime("%A, %B %d, %Y"))
# print("Yarın:", tomorrow.strftime("%B %d, %Y"))
# print(get_date())
# print(get_date(-19))
# print(get_date_w_string(get_date(2)))
# print(get_date_only_number(get_date_w_string(get_date(3))))
