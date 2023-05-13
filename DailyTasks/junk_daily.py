import speech_recognition as sr
import keyboard

def record_audioNote(audio_title, duration="esc"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Lütfen konuşun... Kaydı durdurmak için ESC tuşuna basın.")
        audio = r.listen(source)
        while True:
            try:
                if keyboard.is_pressed('esc') and duration == "esc":
                    break
            except:
                break
    # Buraya çeşitli ayarlamalar gelecek
    with open(f"{audio_title}.wav", "wb") as f:
        f.write(audio.get_wav_data())
