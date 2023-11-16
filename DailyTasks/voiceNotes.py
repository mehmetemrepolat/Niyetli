import pygame
import threading
#from Niyetli.database.db_connector import Database
import time
import mutagen
import os


class VoiceNotes:

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
                # print("thread durdu")
                ## stop iconunun getirilmesi gerekmekte
            thread = threading.Thread(target=play_thread, name="voice_name_thread")
            thread.start()
        except Exception as e:
            print(e)


    def get_voice_duration(self, title):

        audio = mutagen.File(title)
        duration_s = audio.info.length
        return int(duration_s) + 1


    def voice_timer(self, signal=False):
        if signal is not True:
            start = time.time()
            while True:
                passed = time.time() - start
                secs = int(passed % 60)
                mins = int((passed // 60) % 60)
                hours = int(passed // 3600)
                time_str = f"{hours:02d}:{mins:02d}:{secs:02d}"
                time.sleep(1)
                return time_str


    def passingTime(self):
        start = time.time()
        while True:
            passed = time.time() - start
            secs = int(passed % 60)
            mins = int((passed // 60) % 60)
            hours = int(passed // 3600)
            print(f"{hours:02d}:{mins:02d}:{secs:02d}")
            time.sleep(1)

    def name_for_VN(self, title="Yeni Sesli Not", directory="userDirectory/voiceNotes"):
        vn = os.listdir(directory)
        counter = 1

        while True:
            new_title = f"{title} {counter}"
            if any(new_title in file for file in vn):
                counter += 1
            else:
                return new_title







# vc = VoiceNotes()
# vc.play_voice_note("sounds/notification2.wav")

# print(vc.name_for_VN())
# vc.passingTime()
