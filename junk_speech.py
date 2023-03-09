import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Arka plan gürültüsü:" + str(r.energy_threshold))

    try:
        ses = r.listen(source, timeout=2, phrase_time_limit=5)
        print(r.recognize_google(ses, language='tr-tr'))
    except sr.WaitTimeoutError:
        print("Dinleme zaman aşımına uğradı")

    except sr.UnknownValueError:
        print("Ne dediğini anlayamadım")

    except sr.RequestError:
        print("İnternete bağlanamıyorum")