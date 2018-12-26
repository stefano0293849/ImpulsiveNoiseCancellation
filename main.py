#!/usr/bin/env python
# -*- coding: utf-8 -*-


##############################
###### TO DO #################
##############################

# -testare e scegliere i parametri migliori per il clipping



##############################
###### SETTAGGI PROVATI ######
##############################

#RATE = 8000
#CHUNK=4096
#FORMAT = pyaudio.paFloat32
#INFO: buono, avendo un grande chunk ho però maggiore ritardo del suono, per ora è il migliore


#RATE = 44100
#CHUNK=1024
#FORMAT = pyaudio.paInt16
#INFO: buono
#channel=1


##############################
###### APPUNTI ###############
##############################


#WIDTH = 2
# CHANNELS = 2 #numero di campioni usati
# RATE = 11025 #sampling rate, e' il numero di campioni al secondo
# CHUNK=2048 # e' il numero di frame dentro il buffer, in questo caso 1024 bytes,ogni  frame avra' due campioni perche' sono con due canali 
# #il chunk e' come un buffer,e quindi contiene 1024 campioni da due canali e quindi 2048= 1024*2, questo funzionava bene con un valore fisso della prima versione

#questo parametro viene anche chiamato bit depth o sample width = 4 in questo caso
#la grandezza di ogni frame � quindi 8 bytes= 2 canali * 4 bytes per frame
#se io ho un vettore di frame come su https://stackoverflow.com/questions/35970282/what-are-chunks-samples-and-frames-when-using-pyaudio
#ogni elemento dentro questo vettore di frame � 1024 ( chunk) * 8 bytes
#per es un file audio ha un frame = 15 campioni, se ho 7 canali e ogni frame è composto da 2 bytes ( file da 16 bit in)
#allora il bugger è grande 15*2*7
#i dati vengono memorizzati nel buffer in stringht di byte
#ed uso la funzione frombuffer per convertire il buffer da bytes a float a 32 bit in questo caso



#prendo i dati di input , e nel caso in cui venisse identificato un colpo
#il colpo viene sostituito da campioni nulli, il filtro e' a solo scopo dimostrativo
#non viene usato
import wave
import pyaudio
import time
import numpy as np
import collections




CHANNELS = 1 #numero di campioni usati
RATE = 22050 #sampling rate, e' il numero di campioni al secondo
CHUNK=1024*10 # e' il numero di frame dentro il buffer, in questo caso 1024 bytes,ogni  frame avra' due campioni perche' sono con due canali 
#il chunk e' come un buffer,e quindi contiene 1024 campioni da due canali e quindi 2048= 1024*2
#più è grande il rapporto RATE/CHUNK e più ritardo avrò input output


CIRCULAR_BUFFER=10 # vettore contenente 10 medie passate
WAVE_OUTPUT_ORIG="rec_original.wav"
WAVE_OUTPUT_CLIP="rec_clipping.wav"
RECORD_SECONDS = 5 # non usato per ora
FORMAT = pyaudio.paInt16 #ogni campione e' composto da 4 bytes perche' ho scelto 32 bit  ,lo vedo facendo pyaudio.get_sample_size(pyaudio.paFloat32)




zero_vector=np.zeros(CHUNK*CHANNELS)


def bytes_to_float(byte_array):
    int_array = np.frombuffer(byte_array, dtype=np.float32)
    return int_array


def bytes_to_int(byte_array):
    int_array = np.frombuffer(byte_array, dtype=np.int16)
    return int_array

def float_to_bytes(float_array):
    int_array = float_array.astype(np.float32)
    return int_array.tostring()


def int_to_bytes(int_array):
    r_array = int_array.astype(np.int16)
    return r_array.tostring()


def callback(in_data, frame_count, time_info, flag): #funzione usata per processare l'audio
    #in_data sono i dati di input
    #frame_count sono il numero di frame
    global zero_vector
    global old_data_circular_buffer 

    global waveFile_orig    
    global waveFile_clip
    trigger_level=0
   
    #ENABLE TO RECORD ORIGINAL AUDIO AND CLIPPED
    save_audio=0
    
    if(save_audio==1):    
        waveFile_orig.writeframes(in_data)

#    signal = bytes_to_float(in_data)
    signal = bytes_to_int(in_data)
    
    
    #print (max(abs(x) for x in signal))
    #print(len(signal))
#    absolute=max(abs(x) for x in signal) #nuovi dati
    chunk_mean=np.mean(np.absolute(signal))
    
    #print(signal)    
    #print(np.mean(np.absolute(signal)))
    old_data_circular_buffer.append(chunk_mean)
#    trigger_level=max(abs(x) for x in old_data_circular_buffer) #nuovi dati
    trigger_level=np.mean(np.absolute(old_data_circular_buffer))


#    print(absolute)    
    #print(old_data_circular_buffer)
    #print(trigger_level)
    
    if ( (chunk_mean>trigger_level*3) and (chunk_mean>700) ): #da fare un limite adattivo
        signal=zero_vector
        print("BOOOOOOOM")

   
   
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
   
    print("valore medio chunk: %s"%chunk_mean)
    print("valore medio totale: %s"%trigger_level)        





    if(save_audio==1):    
        waveFile_clip.writeframes(signal)


#    output = float_to_bytes(signal)    
    output = int_to_bytes(signal)    
    return (output, pyaudio.paContinue)#in uscita devo dare i dati di uscita ed un flag
    #la lunghezza dei dati in uscita deve esere di frame_count * channels * bytes-per-channel






if __name__ == "__main__":
    
    global old_data_circular_buffer
    global waveFile_orig
    global waveFile_clip    
    p = pyaudio.PyAudio()
    old_data_circular_buffer = collections.deque(maxlen=CIRCULAR_BUFFER) # buffer circolare contenente i valori passati su cui dimensionare l'algoritmo adattivo
    
    waveFile_orig = wave.open(WAVE_OUTPUT_ORIG, 'wb')
    waveFile_orig.setnchannels(CHANNELS)
    waveFile_orig.setsampwidth(p.get_sample_size(FORMAT))
    waveFile_orig.setframerate(RATE)    
    
    waveFile_clip = wave.open(WAVE_OUTPUT_CLIP, 'wb')
    waveFile_clip.setnchannels(CHANNELS)
    waveFile_clip.setsampwidth(p.get_sample_size(FORMAT))
    waveFile_clip.setframerate(RATE) 
    
        
    #print(pyaudio.get_sample_size(pyaudio.paFloat32))
    
    #open mi va' ad aprire uno stream audio
#     stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 output=True,
#                 input=True,
#                 frames_per_buffer=CHUNK, #numero di frames per buffer
#                 stream_callback=callback)
    
    
    
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                frames_per_buffer=CHUNK, #numero di frames per buffer
                stream_callback=callback)    

#    pyaudio.get_sample_size(pyaudio.paFloat32)
    stream.start_stream()
try:
        while stream.is_active():
            time.sleep(5)
            
except KeyboardInterrupt:
        stream.stop_stream() #fermo lo stream e chiamo il distruttore dello stream e della classe pyaduio
        print("\n\nStream is stopped..")
        print("Saving audio..")



#        waveFile.writeframes(b''.join(frames))

        waveFile_orig.close()    
        waveFile_clip.close()         
        stream.close()
        p.terminate()
        print("\nClosed.")

#fai durare il programma per tot secondi
# frames = []
# for i in range(0, int((RATE / CHUNK) * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)


