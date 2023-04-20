import speech_recognition as sr
from WindowControls.MediaControl import MediaControl
# https://www.linkedin.com/feed/update/urn:li:activity:7044235076745707520/


media_control = MediaControl()  # create an instance of the MediaControl class


r = sr.Recognizer()
while True:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Arka plan gürültüsü:" + str(r.energy_threshold))

        try:
            ses = r.listen(source, timeout=2, phrase_time_limit=5)
            cumle = r.recognize_google(ses, language='tr-tr')
            print(r.recognize_google(ses, language='tr-tr'))

            if r.recognize_google(ses, language='tr-tr') == 'Sıradaki şarkı':
                media_control.next_media()
            elif cumle == 'niyetli sesi fulle':
                media_control.set_volume(100)


        except sr.WaitTimeoutError:
            print("Dinleme zaman aşımına uğradı")

        except sr.UnknownValueError:
            print("Ne dediğini anlayamadım")

        except sr.RequestError:
            print("İnternete bağlanamıyorum")