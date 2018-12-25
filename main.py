#prendo i dati di input , e nel caso in cui venisse identificato un colpo
#il colpo viene sostituito da campioni nulli, il filtro è a solo scopo dimostrativo
#non viene usato

import pyaudio
import time
import numpy as np
from scipy.signal import firwin, firwin2, lfilter, freqz

WIDTH = 2
CHANNELS = 2
RATE = 11025

p = pyaudio.PyAudio()
f1 = 500/1000

zero_vector=np.zeros(2048)

def bytes_to_float(byte_array):
    int_array = np.frombuffer(byte_array, dtype=np.float32)
    return int_array

def float_to_bytes(float_array):
    int_array = float_array.astype(np.float32)
    return int_array.tostring()

def callback(in_data, frame_count, time_info, flag):
    global zero_vector
    signal = bytes_to_float(in_data)
    #print (max(abs(x) for x in signal))
    #print(len(signal))
    absolute=max(abs(x) for x in signal)
    if(absolute>0.3):
        filtered=zero_vector
        
        
    else:
        a = [1]
        b = firwin(129, f1, pass_zero=False)
        #filtered= lfilter(b, a, signal) #segnale filtrao in bytes
        filtered=signal

    output = float_to_bytes(filtered) #segnale filtrato convertito da bytes to float
    
    print(max(abs(x) for x in filtered))
    return (output, pyaudio.paContinue)

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