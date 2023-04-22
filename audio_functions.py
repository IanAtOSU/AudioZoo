import wave
import audioop
import numpy as np
import os

'''
Notes:
    - All functions take a range from 0-1 as their multiplier input
'''

def filenamefrompath(name):
    result=""
    for c in name:
        if c=='/' or c=='\\':
            result=""
        else:
            result+=c
    return result

#Changes the audio file's volume
def changeVolume(audio_path, sprite_hash, multiplier):
    multiplier = multiplier*2 #Range from 0 to 2

    audioIn = wave.open(audio_path, 'rb')
    p = audioIn.getparams()

    outpath = "Sounds/Out/VolOut_" + str(sprite_hash) + audio_path[audio_path.rfind("/")+1:]

    audioOut = wave.open(outpath, 'wb')
    audioOut.setparams(p)
    frames = audioIn.readframes(p.nframes)
    audioOut.writeframesraw(audioop.mul(frames, p.sampwidth, multiplier))
    return outpath

#Pitches the audio file up or down
def changePitch(audio_path, sprite_hash, multiplier):
    Hz_shift = (multiplier-0.5)*1200 #range of change from -600 to +600 Hertz
    audioIn = wave.open(audio_path, 'rb')
    p = list(audioIn.getparams())
    p[3] = 0 #(Number of samples will be set by writeframes)

    outpath = "Sounds/Out/PitchOut_" + str(sprite_hash) + audio_path[audio_path.rfind("/")+1:]

    audioOut = wave.open(outpath, 'w')
    audioOut.setparams(tuple(p))

    #Audio processing:
    frac = 20 #process in fractions of a second to avoid reverb.
    size = audioIn.getframerate()//frac
    sections = int(audioIn.getnframes()/size) #sections of file
    shift = int(Hz_shift//frac)

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
    return outpath

def changeSpeed(audio_path, sprite_hash, multiplier):
    multiplier = pow(multiplier,2)*3+0.25 #range from 0.25x to 3.25x
    audioIn = wave.open(audio_path, 'rb')
    rate = audioIn.getframerate()
    frames = audioIn.readframes(-1)

    outpath = "Sounds/Out/SpeedOut_" + str(sprite_hash) + audio_path[audio_path.rfind("/")+1:]

    audioOut = wave.open(outpath, 'wb')

    audioOut.setparams(audioIn.getparams())
    audioOut.setframerate(int(rate*multiplier))
    audioOut.writeframes(frames)
    audioIn.close()
    audioOut.close()
    return outpath

def deleteOutfiles():
    for f in os.listdir("Sounds/Out"):
        os.remove(os.path.join("Sounds/Out", f))