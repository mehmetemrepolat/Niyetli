from win32gui import GetWindowText, GetForegroundWindow
import time
import psutil
import win32process

Programs = []  # Çalışan program isimleri listesi
Times = []  # Çalışma sürelerini tutmak için liste

def get_ForeGroundApp():
    if psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "") == 'explorer':
        hwnd = GetForegroundWindow()
        title = GetWindowText(hwnd)
        return title

    else:
        return psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")


def get_App_index(app):
    return Programs.index(app) if app in Programs else -1

def is_ForeGroundApp_get_change():
    ForeGround_App = get_ForeGroundApp()
    if ForeGround_App not in Programs:
        Programs.append(ForeGround_App)
        Times.append(0)
    app_index = get_App_index(ForeGround_App)
    Times[app_index] += 1

def secreen_timer():
    while True:
        try:
            is_ForeGroundApp_get_change()
        except:
            pass
        print(Programs, " - ", Times)
        time.sleep(1)

secreen_timer()
    # Veritabanına ekleme yapılacak şekilde olacak. Bu ekleme günün belirli saatinde gerçekleştirilecek.
    # Veritabanına eklenememesi veya bağlantı hatası gibi konular konusuna önlem olarak Not Defteri veya excel tablosu gibi
    # yapı kullanılıp 'Ram Yedek' şeklinde muhafaza edilecek.
    # Veritabanında bir adet tablo olacak içerisine veriler ekleme yapılacak.
    # Her bir programın kendisine ait id'si olacak ve o id'ler Prime Key olarak atanacak.
    # Daha sonraki evrelerde kullanıcı secreen timer özelliğinden faydalanmak istediğinde
    # Veritabanından bütün programlara ait ekran sürelerini hesaplayarak(belirli aralık da çekilebilir.)
    # Kullanıcıya tablo şeklinde sunacak. Veya Niyetli bunu kullanıcıya sesli bir şekilde iletecek.
