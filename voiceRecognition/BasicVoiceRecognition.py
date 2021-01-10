import wave
from datetime import datetime

import speech_recognition as sr
import pyaudio



#r.recognize_google()

def record_responce():
    r = sr.Recognizer()
    CHUNK = 1024
    WIDTH = 2
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    FORMAT = pyaudio.paInt16

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)
    print("here")
    print(f"* recording {datetime.now()}")
    chunks = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)  #read audio stream
        chunks.append(data)
        #stream.write(data, CHUNK)  #play back audio stream

    print(f"* done {datetime.now()}")
    wf = wave.open("undentified.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(chunks))
    wf.close()

    stream.stop_stream()
    stream.close()

    p.terminate()
    with sr.AudioFile('undentified.wav') as source:
        audio = r.record(source)

    return r.recognize_google(audio)



