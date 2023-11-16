import pygame
import time

pygame.init()

# Ses dosyasının adını belirtin
ses_dosyasi = "sounds/alarm1.wav"

# Pygame ses sistemi üzerinden sesi yükle
pygame.mixer.music.load(ses_dosyasi)

# Ses dosyasını belirli bir süre boyunca sürekli çal
calma_suresi = 10  # saniye
pygame.mixer.music.play(loops=-1)  # loops=-1, sesin sürekli çalmasını sağlar

# Belirtilen süre boyunca bekleyin
time.sleep(calma_suresi)

# Ses çalma işlemi bittiğinde pygame'i kapat
pygame.mixer.music.stop()
pygame.quit()
