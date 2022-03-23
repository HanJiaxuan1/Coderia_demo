import os
import subprocess

# Aim：这个py用来将mp3转为wav

# 将input下的所有mp3文件转wav
def ffmpeg_MP3ToWav(input_path, output_path):
    # 提取input_path路径下所有文件名
    filename = os.listdir(input_path)
    for file in filename:
        path1 = input_path + "\\" + file
        path2 = output_path + "\\" + os.path.splitext(file)[0]
        cmd = "D:/ffmpeg/bin/ffmpeg -i " + path1 + " " + "-ac 1 -ar 16000 " + path2 + ".wav" # 将input_path路径下所有音频文件转为.wav文件
        subprocess.call(cmd, shell=True)

def MP4ToWav(input_path, output_path, filename):
    path1 = input_path + "\\" + filename
    path2 = output_path + '\\' + os.path.splitext(filename)[0]
    # 将MP3转为 单声道 16000 采样率 的wav文件
    # API要求文档 https://ai.baidu.com/ai-doc/SPEECH/7k38lxpwf
    cmd = "D:/ffmpeg/bin/ffmpeg -i " + path1 + " " + "-ac 1 -ar 16000 " + path2 + ".wav"
    subprocess.Popen(cmd, shell=True)

# input_path = r"D:\PycharmProject\testForDegree\resource"
# output_path = r"D:\PycharmProject\testForDegree\resource"
# MP4ToWav(input_path, output_path, 'English.mp3')