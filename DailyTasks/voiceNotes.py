import pygame
import threading
# from Niyetli.database.db_connector import Database
from mutagen.mp3 import MP3


class VoiceNotes:
    # dib = Database()

    def play_voice_note(self, path):
        print("Yol:", path)
        duration = self.get_voice_duration(path)
        print("Durdurma zamanı:", duration)
        try:
            def play_thread():
                pygame.mixer.init()
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
                # Burada stop kısmını eklememiz gerekiyor
                #time.sleep(duration)
                #print("thread durdu")
                ## stop iconunun getirilmesi gerekmekte
            thread = threading.Thread(target=play_thread, name="voice_name_thread")
            thread.start()

        except Exception as e:
            print(e)


    def get_voice_duration(self, voice_path):
        audio = MP3(voice_path)
        duration_s = audio.info.length
        return int(duration_s) + 1


vc = VoiceNotes()
print(vc.get_voice_duration("johncena.mp3"))
