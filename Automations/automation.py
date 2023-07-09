import threading
import time
from Niyetli.WindowControls.MediaControl import MediaControl, WindowsOsControl
from Niyetli.DailyTasks.AlarmCalendarReminderOP import DateOperations

# Sesli bir şekilde otomasyon gerçekleştirme
# Gece uyumaya yakın müzik dinleme otomasyonu - Belli bir süre sonra müziği durdurma
# Belirli saatler sonrası herhangi bir işlem gerçekleşmediği taktirde bilgisayarı kapatma, bekleme moduna alma
# Konuma göre otomasyon olabilir

class UserAutomation:

    @staticmethod
    def turn_of_music(minute):  # Dakika
        stop_time = minute
        SB = DateOperations()

        def stop():
            mc = MediaControl()
            mc.play_pause_media()
        threading.Timer(stop_time, stop).start()
        SB.show_balloon("Niyetli'den Mesaj", f"Medya {stop_time} dakika sonra durdurulacaktır.")

    @staticmethod
    def sleep_mode(minute):  # Dakika
        stop_time = minute
        SB = DateOperations()

        def sleep():
            woc = WindowsOsControl()
            woc.shutdown_system()
        threading.Timer(stop_time, sleep).start()
        SB.show_balloon("Niyetli'den Önemli", f"Bilgisayar {stop_time} dakika sonra uyku moduna geçecektir.")

class NiyetliAutomation:
    pass
    # Bu otomasyonlar kullanıcının sık sık ziyaret ettiği sayfalar veya programlar işlenecek.
    # Kullanıcı ilk olarak hangi programı açıyor? Bu programda kaç dakika kalıyor?
    # Yapılan işlem izlenebilir mi? İzlenebilirse, yapılan işlem otomasyona geçirilebilir mi?
    # Kullanıcı ses seviyesini nasıl ayarlıyor? Hangi saatlerde yüksek sesli müzik dinliyor?
    # Kullanıcı ekran parlaklığını nasıl ayarlıyor? hangi saatlerde veya hangi programlarda yüksek parlaklık açıyor?
    # Bu gibi sorulara cevaplar bulunabiliyor mu? önce bu kontrol edilecek daha sonrasında buraya işlenecek
    # Sorular daha fazla arttırılacak.


a = UserAutomation()

a.turn_of_music(25)
a.sleep_mode(26)

