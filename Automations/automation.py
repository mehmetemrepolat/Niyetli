import threading
import time
from Niyetli.WindowControls.MediaControl import MediaControl, WindowsOsControl
from Niyetli.DailyTasks.AlarmCalendarReminderOP import DateOperations

# Sesli bir şekilde otomasyon gerçekleştirme
# Gece uyumaya yakın müzik dinleme otomasyonu - Belli bir süre sonra müziği durdurma
# Belirli saatler sonrası herhangi bir işlem gerçekleşmediği taktirde bilgisayarı kapatma, bekleme moduna alma
# Konuma göre otomasyon olabilir

class Automation:

    @staticmethod
    def turn_of_music(minute):  # Dakika
        stop_time = minute * 60
        SB = DateOperations()

        def stop():
            mc = MediaControl()
            mc.play_pause_media()
        threading.Timer(stop_time, stop).start()
        SB.show_balloon("Niyetli'den Mesaj", f"Medya {stop_time} dakika sonra durdurulacaktır.")

    @staticmethod
    def sleep_mode(minute):  # Dakika
        stop_time = minute * 60
        SB = DateOperations()

        def sleep():
            woc = WindowsOsControl()
            woc.sleep_system()
        threading.Timer(stop_time, sleep).start()
        SB.show_balloon("Niyetli'den Önemli", f"Bilgisayar {stop_time} dakika sonra uyku moduna geçecektir.")

    


a = Automation()

a.turn_of_music(1)
a.sleep_mode(2)
a = 0
while True:
    a += 1
    time.sleep(1)
    print(a)
