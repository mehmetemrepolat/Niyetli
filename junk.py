import time
import threading

def hatirlatici(saniye):
    time.sleep(saniye)
    print("Hatırlatıcı: {} saniye doldu!".format(saniye))

def farkli_metot():
    x = 1
    while True:
        time.sleep(1)
        x += 1
        print(x)

def ana_program():
    while True:
        secim = input("Hangi işlemi yapmak istersiniz?\n 1. Hatırlatıcıyı başlat\n 2. Başka bir metodu çalıştır\n 3. Çıkış\nSeçiminiz: ")

        if secim == "1":
            saniye = int(input("Hatırlatıcı kaç saniye sonra çalışsın?: "))
            t = threading.Thread(target=hatirlatici, args=(saniye,))
            t.start()

        elif secim == "2":
            farkli_metot()

        elif secim == "3":
            print("Program sonlandırıldı.")
            break

        else:
            print("Geçersiz seçim! Tekrar deneyin.")

ana_program()
