
class voiceNotes:
    import pygame
    import threading
    from Niyetli.database.db_connector import Database
    from mutagen.mp3 import MP3


    db = Database()

    def play_voice_note(self, voice_title):
        print("Deneme")
        try:
            path = self.db.get_sound_from_db(voice_title)
            print("yol:", path)

            def play_thread():
                self.pygame.mixer.init()
                self.pygame.mixer.music.load(path)
                self.pygame.mixer.music.play()
                # Burada stop kısmını eklememiz gerekiyor

            thread = self.threading.Thread(target=play_thread)
            thread.start()
        except Exception as e:
            print(e)


    def get_voice_duration(self, voice_path):
        audio = self.MP3(voice_path)
        duration_s = audio.info.length
        return int(duration_s) + 1


# vc = VoiceNotes()
# print(vc.get_voice_duration("johncena.mp3"))

