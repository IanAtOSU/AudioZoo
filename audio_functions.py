import wave
import audioop

def changeVolume(audio_path, multiplier):
    audioIn = wave.open("Sounds/" + audio_path, 'rb')
    p = audioIn.getparams()
    audioOut = wave.open("audioOutput/" + audio_path, 'wb')
    audioOut.setparams(p)
    frames = audioIn.readframes(p.nframes)
    audioOut.writeframesraw(audioop.mul(frames, p.sampwidth, multiplier))





changeVolume("testAudio.wav", 0.25)

