#prendo i dati di input e li butto semplicemente in uscita

import pyaudio
import time
import numpy as np
import scipy.signal as signal



def callback(in_data, frame_count, time_info, flag):
    global b,a,fulldata #global variables for filter coefficients and array
    audio_data = np.fromstring(in_data, dtype=np.float32)
    #do whatever with data, in my case I want to hear my data filtered in realtime
    audio_data = signal.filtfilt(b,a,audio_data,padlen=200).astype(np.float32).tostring()
    fulldata = np.append(fulldata,audio_data) #saves filtered data in an array
    return (audio_data*2, pyaudio.paContinue)




CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()
b,a=signal.iirdesign(0.03,0.07,5,40)
fulldata = np.array([])



stream = p.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(10)

stream.stop_stream()
print("Stream is stopped")
stream.close()
p.terminate()