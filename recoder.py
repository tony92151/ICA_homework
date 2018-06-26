
import pyaudio
import wave


############################################################################
#audio recoding

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output1.wav"
WAVE_OUTPUT_FILENAME2 = "output2.wav"

p = pyaudio.PyAudio()



stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
stream2 = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("open all mircophone")


print("* recording")

frames = []
frames2 = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    data2 = stream2.read(CHUNK)
    frames2.append(data2)

print (frames)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
wf2 = wave.open(WAVE_OUTPUT_FILENAME2, 'wb')
wf2.setnchannels(CHANNELS)
wf2.setsampwidth(p.get_sample_size(FORMAT))
wf2.setframerate(RATE)
wf2.writeframes(b''.join(frames2))
wf2.close()

