import ctypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class MediaControl:
    def set_volume(self, volume):  # Bu kısım daha sonrasında sesli komutlara göre uyumlu hale getirilecek
        """Ses Yükseklik Kontrolleri"""
        if volume < 0 or volume > 100:
            print("0-100 arasında bir sayı girin!")
        else:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume_object = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            volume_object.SetMasterVolumeLevelScalar(volume / 100, None)


    def play_pause_media(self):
        """Medya durdur/oynat."""
        ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)  # Play/Pause tuşu
        ctypes.windll.user32.keybd_event(0xB3, 0, 0x0002, 0)


    def next_media(self):
        """Sonraki medya parçası"""
        ctypes.windll.user32.keybd_event(0xB0, 0, 0, 0)  # Forward tuşu
        ctypes.windll.user32.keybd_event(0xB0, 0, 0x0002, 0)


    def previous_media(self):
        """Önceki medya parçası"""
        ctypes.windll.user32.keybd_event(0xB1, 0, 0, 0)  # Backward tuşu
        ctypes.windll.user32.keybd_event(0xB1, 0, 0x0002, 0)

#set_volume(50)
# next_media()
# play_pause_media()
# previous_media()



