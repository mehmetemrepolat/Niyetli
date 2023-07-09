import pyaudio
import wave
import os

def mp3_to_wav(mp3_file, wav_file):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=2, rate=44100, input=False, output=True, frames_per_buffer=1024)
    with open(mp3_file, 'rb') as f:
        stream.write(f.read())
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Sesi wav dosyasına kaydet
    os.rename('stream.wav', wav_file)

if __name__ == "__main__":
    mp3_file = "userDirectory/voiceNotes/merhabalar.mp3"  # Dönüştürülecek mp3 dosyasının adı
    wav_file = "sesdosyasi.wav"  # Dönüştürülen wav dosyasının adı

    mp3_to_wav(mp3_file, wav_file)
