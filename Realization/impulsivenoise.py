#!/usr/bin/env python
# -*- coding: utf-8 -*-



#dependency
#if pip install pyaudio doesn't work, do in the following way to install them from the cmd:
#download pyaudio from https://www.lfd.uci.edu/~gohlke/pythonlibs/ and then in the cmd use "pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl"
#"pip install numpy"
import wave
import pyaudio
import time
import numpy as np
import collections
from math import *





##############################
######     SETTINGS     ######
##############################

VERSION=2.4
CHANNELS = 1 
RATE = 22050 #sampling rate
CHUNK=8000 # is the number of frame inside the buffer



CIRCULAR_BUFFER=10 #the vector that hold the last 10 chunks
WAVE_OUTPUT_ORIG="rec_original.wav"
WAVE_OUTPUT_CLIP="rec_clipping.wav"
RECORD_SECONDS = 5 # non used for now
FORMAT = pyaudio.paInt16 #format of the audio
COMPRESSOR_FACTOR=10
save_audio=1 #enable to save the filtered and original audio files

#zero audio chunk to use when input sound is over the trigger level
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


##############################
######     CALL BACK    ######
##############################

def callback(in_data, frame_count, time_info, flag): #this function is used to process the audio, it is executed in a different thread from the main
    #in_data are the input data
    #frame_count is the number of frames
    global zero_vector
    global old_data_circular_buffer 
    global old_data
    global waveFile_orig    
    global waveFile_clip
    global i
    global x
    trigger_level=0
    
#ENABLE TO RECORD ORIGINAL AUDIO AND CLIPPED
    global save_audio
    
    
    #i'll save the original audio with out the filter    
    if(save_audio==1):    
        waveFile_orig.writeframes(in_data)
        
        
    #converter received data to int for processing it

    signal = bytes_to_int(in_data)
    chunk_mean=np.mean(np.absolute(signal))  
    old_data_circular_buffer.append(chunk_mean)

    #i'll update the trigger level in base the mean of the last values
    trigger_level=np.mean(np.absolute(old_data_circular_buffer))


    #if there is the impulsive noise: 
    if ( (chunk_mean>trigger_level*2.5) and (chunk_mean>1000) ): 
        print("Shot Detected")
    #if the choosen algorithm is the clipping :
        if(x==0):
            signal=zero_vector

    #if the choosen algorithm is the old data :
        if(x==1): 
            signal=old_data

    #if the choosen algorithm is the compressor :  
        if(x==2):             
           signal=(signal)/ int (( np.log10(chunk_mean)*COMPRESSOR_FACTOR    ))



            

    #if there isn't the impulsive noise:        
    else:
        #and you are using the algorithm with the old data, save the chunk on the circolar buffer to update the trigger level      
        if(x==1):
            old_data=signal            
            

      
          
    # print("valore medio chunk: %s"%chunk_mean)
    #print("valore medio totale: %s"%trigger_level)  
    
    
   
    output = int_to_bytes(signal) 
    
    #save the filtered audio if the option is enabled
    if(save_audio==1):    
        waveFile_clip.writeframes(output)    
                
    return (output, pyaudio.paContinue)#return of the function




##############################
######       MAIN       ######
##############################

if __name__ == "__main__":
    
    global old_data_circular_buffer
    global waveFile_orig
    global waveFile_clip  
    global old_data
    global i
    global x
    i=0
    old_data=zero_vector
   
   #art output just to keep track of the version (and also becouse is cool)
    print("""\


 _____                      _     _             _   _       _           ______         _            _   _             
|_   _|                    | |   (_)           | \ | |     (_)          | ___ \       | |          | | (_)            
  | | _ __ ___  _ __  _   _| |___ ___   _____  |  \| | ___  _ ___  ___  | |_/ /___  __| |_   _  ___| |_ _  ___  _ __  
  | || '_ ` _ \| '_ \| | | | / __| \ \ / / _ \ | . ` |/ _ \| / __|/ _ \ |    // _ \/ _` | | | |/ __| __| |/ _ \| '_ \ 
 _| || | | | | | |_) | |_| | \__ \ |\ V /  __/ | |\  | (_) | \__ \  __/ | |\ \  __/ (_| | |_| | (__| |_| | (_) | | | |
 \___/_| |_| |_| .__/ \__,_|_|___/_| \_/ \___| \_| \_/\___/|_|___/\___| \_| \_\___|\__,_|\__,_|\___|\__|_|\___/|_| |_|
               | |                                                                                                    
               |_|                                                                                             """+"V. "+str(VERSION)+"\n\n\n"                                                                                                 

         )
    

    
    x = int (input("Choose the  algorithm to use:  zero[0] , old value[1] or  compressor[2] : "))  
    p = pyaudio.PyAudio()
    # circular buffer , used to update the adaptive trigger level
    old_data_circular_buffer = collections.deque(maxlen=CIRCULAR_BUFFER) 
    
    #inizialize the output file
    waveFile_orig = wave.open(WAVE_OUTPUT_ORIG, 'wb')
    waveFile_orig.setnchannels(CHANNELS)
    waveFile_orig.setsampwidth(p.get_sample_size(FORMAT))
    waveFile_orig.setframerate(RATE)    
    
    waveFile_clip = wave.open(WAVE_OUTPUT_CLIP, 'wb')
    waveFile_clip.setnchannels(CHANNELS)
    waveFile_clip.setsampwidth(p.get_sample_size(FORMAT))
    waveFile_clip.setframerate(RATE) 
    
        
   #open the input stream from the mic
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                #number of frames into the buffer
                frames_per_buffer=CHUNK, 
                stream_callback=callback)    


    #and while input stream is streaming, output the returned data from the callback function to the loudspeaker
    stream.start_stream()
try:
        while stream.is_active():
            time.sleep(5)
            
except KeyboardInterrupt:
        #stop of the stream
        stream.stop_stream() 
        print("\n\nStream is stopped..")
        print("Saving audio..")
        waveFile_orig.close()    
        waveFile_clip.close()         
        stream.close()
        p.terminate()
        print("\nClosed.")
