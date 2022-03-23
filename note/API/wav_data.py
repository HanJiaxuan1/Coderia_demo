import os
import wave
import ffmpeg

def getFrameRate(file):
    f = wave.open(file)
    frameRate = f.getframerate()
    print(frameRate)
    return frameRate

# 将音频采样率统一为16kHz （安装Baidu API要求）
def filePre(file):
    frameRate = getFrameRate(file)
    newFile = ''
    if frameRate != 16000:
        newFile = str.split(file,'.')[0] + '_new.wav'
        ffmpeg.input(file).output(newFile, ar=16000).run()
    return newFile

getFrameRate('../static/resource/Chinese.wav')