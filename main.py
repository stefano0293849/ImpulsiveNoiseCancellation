#!/usr/bin/env python
# -*- coding: utf-8 -*-


##############################
###### TO DO #################
##############################

# -testare


##############################
###### SETTAGGI PROVATI ######
##############################

#RATE = 8000
#CHUNK=4096
#FORMAT = pyaudio.paFloat32
#INFO: buono, avendo un grande chunk ho però maggiore ritardo del suono, per ora è il migliore

#prendo i dati di input , e nel caso in cui venisse identificato un colpo
#il colpo viene sostituito da campioni nulli, il filtro e' a solo scopo dimostrativo
#non viene usato

import pyaudio
import time
import numpy as np
import collections
#from scipy.signal import firwin, firwin2, lfilter, freqz

#WIDTH = 2
# CHANNELS = 2 #numero di campioni usati
# RATE = 11025 #sampling rate, e' il numero di campioni al secondo
# CHUNK=2048 # e' il numero di frame dentro il buffer, in questo caso 1024 bytes,ogni  frame avra' due campioni perche' sono con due canali 
# #il chunk e' come un buffer,e quindi contiene 1024 campioni da due canali e quindi 2048= 1024*2


CHANNELS = 1 #numero di campioni usati
RATE = 8000 #sampling rate, e' il numero di campioni al secondo
CHUNK=4096 # e' il numero di frame dentro il buffer, in questo caso 1024 bytes,ogni  frame avra' due campioni perche' sono con due canali 
#il chunk e' come un buffer,e quindi contiene 1024 campioni da due canali e quindi 2048= 1024*2
CIRCULAR_BUFFER=10 # vettore contenente 10 medie passate





RECORD_SECONDS = 5 # non usato per ora
FORMAT = pyaudio.paFloat32 #ogni campione e' composto da 4 bytes perche' ho scelto 32 bit  ,lo vedo facendo pyaudio.get_sample_size(pyaudio.paFloat32)



#questo parametro viene anche chiamato bit depth o sample width = 4 in questo caso
#la grandezza di ogni frame � quindi 8 bytes= 2 canali * 4 bytes per frame
#se io ho un vettore di frame come su https://stackoverflow.com/questions/35970282/what-are-chunks-samples-and-frames-when-using-pyaudio
#ogni elemento dentro questo vettore di frame � 1024 ( chunk) * 8 bytes

#per es un file audio ha un frame = 15 campioni, se ho 7 canali e ogni frame è composto da 2 bytes ( file da 16 bit in)
#allora il bugger è grande 15*2*7


#i dati vengono memorizzati nel buffer in stringht di byte
#ed uso la funzione frombuffer per convertire il buffer da bytes a float a 32 bit in questo caso



zero_vector=np.zeros(CHUNK*CHANNELS)


def bytes_to_float(byte_array):
    int_array = np.frombuffer(byte_array, dtype=np.float32)
    return int_array

def float_to_bytes(float_array):
    int_array = float_array.astype(np.float32)
    return int_array.tostring()

def callback(in_data, frame_count, time_info, flag): #funzione usata per processare l'audio
    #in_data sono i dati di input
    #frame_count sono il numero di frame
    global zero_vector
    global old_data_circular_buffer 
    trigger_level=0
    
    signal = bytes_to_float(in_data)
    #print (max(abs(x) for x in signal))
    #print(len(signal))
#    absolute=max(abs(x) for x in signal) #nuovi dati
    chunk_mean=np.mean(np.absolute(signal))
    
    #print(signal)    
    #print(np.mean(np.absolute(signal)))
    old_data_circular_buffer.append(chunk_mean)
#    trigger_level=max(abs(x) for x in old_data_circular_buffer) #nuovi dati
    trigger_level=np.mean(np.absolute(old_data_circular_buffer))
    print("valore medio chunk: %s"%chunk_mean)
    print("valore medio totale: %s"%trigger_level)

#    print(absolute)    
    #print(old_data_circular_buffer)
    #print(trigger_level)
    
    if (chunk_mean>trigger_level*2): #da fare un limite adattivo
        signal=zero_vector
#       filtered=zero_vector
   
   
#callback per trovare il valore medio del chunk   
# def callback(in_data, frame_count, time_info, status):
#     levels = []
#     for _i in range(1024):
#         levels.append(struct.unpack('<h', in_data[_i:_i + 2])[0])
#     avg_chunk = sum(levels)/len(levels)
#     
#     print_audio_level(avg_chunk, time_info['current_time'])
#     
#     return (in_data, pyaudio.paContinue)   
   
        
        
#    else:
    #print("il livello di trigger vale %s,valore attuale %s"%(trigger_level,max(abs(x) for x in filtered)))
#    output = float_to_bytes(filtered) #segnale filtrato convertito da bytes to float
    output = float_to_bytes(signal)    

    return (output, pyaudio.paContinue)#in uscita devo dare i dati di uscita ed un flag
    #la lunghezza dei dati in uscita deve esere di frame_count * channels * bytes-per-channel






if __name__ == "__main__":
    
    global old_data_circular_buffer 
    p = pyaudio.PyAudio()
    old_data_circular_buffer = collections.deque(maxlen=CIRCULAR_BUFFER) # buffer circolare contenente i valori passati su cui dimensionare l'algoritmo adattivo
    
    
    
    #print(pyaudio.get_sample_size(pyaudio.paFloat32))
    
    #open mi va' ad aprire uno stream audio
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                frames_per_buffer=CHUNK, #numero di frames per buffer
                stream_callback=callback)

#    pyaudio.get_sample_size(pyaudio.paFloat32)
    stream.start_stream()

    while stream.is_active():
        time.sleep(10)


#fai durare il programma per tot secondi
# frames = []
# for i in range(0, int((RATE / CHUNK) * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)


    stream.stop_stream() #fermo lo stream e chiamo il distruttore dello stream e della classe pyaduio
    print("Stream is stopped")
    stream.close()
    p.terminate()