#programa semplice per prendere l'input e buttarlo in output senza filtro

import pyaudio
import numpy as np
import time
 
p = pyaudio.PyAudio()
 
CHANNELS = 2
RATE = 8000
 
def callback(in_data, frame_count, time_info, flag):
    # using Numpy to convert to array for processing
    # audio_data = np.fromstring(in_data, dtype=np.float32)
    return (in_data, pyaudio.paContinue)
 

#open stream using callback
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

