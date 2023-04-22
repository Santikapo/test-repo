from playsound import playsound
import pyaudio
import wave
import struct


echolen = 1000

# the file name output you want to record into
filename = "recorded.wav"
# set the chunk size of 1024 samples
chunk = 1
# sample format
FORMAT = pyaudio.paInt16
# mono, change to 2 if you want stereo
channels = 1
# 44100 samples per second
sample_rate = 44100
record_seconds = 3
# initialize PyAudio object
p = pyaudio.PyAudio()
# open stream object as input & output
stream = p.open(format=FORMAT,
                channels=channels,
                rate=sample_rate,
                input=True,
                output=True,
                frames_per_buffer=chunk)
frames = []
print("Recording...")
counter = 0;
echo = []

for i in range(echolen):        
    echo.append(0)
    
flip = True

for i in range(int(sample_rate / chunk * record_seconds)):
    data = stream.read(chunk)


    data1 = struct.unpack('h', data)[0]

    data2 = struct.pack('h', data)


    # if you want to hear your voice while recording
    # stream.write(data)
    frames.append(data2)
    counter += 1
    
    #if (data1 > 10 and data1 != 65535):
     #   print(data, type(data))
      #  print(data1, type(data1))
     #   break




print("Finished recording.")
# stop and close stream
stream.stop_stream()
stream.close()
# terminate pyaudio object
p.terminate()
# save audio file
# open the file in 'write bytes' mode
wf = wave.open(filename, "wb")
# set the channels
wf.setnchannels(channels)
# set the sample format
wf.setsampwidth(p.get_sample_size(FORMAT))
# set the sample rate
wf.setframerate(sample_rate)
# write the frames as bytes
wf.writeframes(b"".join(frames))
# close the file
wf.close()


"""temp = data1


    if counter == echolen:
        counter = 0

    buffer = data1 + echo[counter]
    echo[counter] = int(temp + echo[counter]/2)
"""