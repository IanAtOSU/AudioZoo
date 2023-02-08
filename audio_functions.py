import wave
import audioop
import numpy as np
import os

#Changes the audio file's volume
def changeVolume(audio_path, multiplier):
    audioIn = wave.open("Sounds/" + audio_path, 'rb')
    p = audioIn.getparams()
    os.remove("audioOutput/" + audio_path) #Ensure that this file isn't already there
    audioOut = wave.open("audioOutput/" + audio_path, 'wb')
    audioOut.setparams(p)
    frames = audioIn.readframes(p.nframes)
    audioOut.writeframesraw(audioop.mul(frames, p.sampwidth, multiplier))

#Pitches the audio file up or down
def changePitch(audio_path, Hz_shift):
    audioIn = wave.open("Sounds/" + audio_path, 'r')
    p = list(audioIn.getparams())
    p[3] = 0 #(Number of samples will be set by writeframes)
    os.remove("audioOutput/" + audio_path) #Ensure that this file isn't already there
    audioOut = wave.open("audioOutput/" + audio_path, 'w')
    audioOut.setparams(tuple(p))

    #Audio processing:
    frac = 20 #process in fractions of a second to avoid reverb.
    size = audioIn.getframerate()//frac
    sections = int(audioIn.getnframes()/size) #sections of file
    shift = Hz_shift//frac

    #Get the data and split into left and right audio channels
    for n in range(sections):
        data = np.frombuffer(audioIn.readframes(size), dtype=np.int16)
        left, right = data[0::2], data[1::2]
        
        #Get ther frequencies using Fast Fourier Transform
        lf, rf = np.fft.rfft(left), np.fft.rfft(right)
        #Rolling the array increases the pitch
        lf, rf = np.roll(lf, shift), np.roll(rf, shift)
        #We don't want the highest frequencies to roll over to the lowest ones so we'll 0 them
        if(shift > 0):
            lf[0:shift], rf[0:shift] = 0, 0
        else:
            lf[len(lf)-shift:len(lf)], rf[len(rf)-shift:len(rf)] = 0, 0
        #Convert signal back into amplitude
        nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
        #Put the two channels together
        final = np.column_stack((nl,nr)).ravel().astype(np.int16)
        audioOut.writeframes(final.tobytes())

    audioIn.close()
    audioOut.close() 

def changeSpeed(audio_path, multiplier):
    audioIn = wave.open("Sounds/" + audio_path, 'rb')
    rate = audioIn.getframerate()
    frames = audioIn.readframes(-1)
    os.remove("audioOutput/" + audio_path) #Ensure that this file isn't already there
    audioOut = wave.open("audioOutput/" + audio_path, 'wb')

    audioOut.setparams(audioIn.getparams())
    audioOut.setframerate(rate*multiplier)
    audioOut.writeframes(frames)
    audioIn.close()
    audioOut.close()


changeVolume("TestAudio.wav", 0.25)
changePitch("TestAudio.wav", -100)
changeSpeed("TestAudio.wav", 2)