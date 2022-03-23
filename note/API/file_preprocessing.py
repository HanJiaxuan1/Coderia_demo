import os
import wave
import ffmpeg

# Aim：这个py用来切割wav文件
# https://blog.csdn.net/xuqingda/article/details/86540333?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2.pc_relevant_antiscan&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2.pc_relevant_antiscan&utm_relevant_index=5


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


def get_duration(file):
    f = wave.open(file)
    rate = f.getframerate()
    frames = f.getnframes()
    duration = frames / float(rate)  # 单位为s
    return duration


def audio_cut(audio_in_path, audio_out_path, start_time, dur_time):
    """
    :param audio_in_path: 输入音频的绝对路径
    :param audio_out_path: 切分后输出音频的绝对路径
    :param start_time: 切分开始时间
    :param dur_time: 切分持续时间
    :return:
    """
    os.system("D:/ffmpeg/bin/ffmpeg -i {in_path} -vn -acodec copy -ss {Start_time} -t {Dur_time}  {out_path}".format(in_path = audio_in_path,
                out_path = audio_out_path, Start_time = start_time, Dur_time = dur_time))


def main():
    audio_in_dir = r"D:\PycharmProject\testForDegree\static\resource"   #要切割的文件列表
    audio_out_dir = r"D:\PycharmProject\testForDegree\temp" #输入文件夹
    start_time = 0 #切割开始时间
    dur_time = 20  #切割的片段时长s
    out_number = 0 #输出文件序号
    audio_in_name = "test.wav"  #逐个要切割的文件名
    print(audio_in_name)
    audio_in_path = audio_in_dir + "/" + audio_in_name
    print(audio_in_path)
    audio_length = get_duration(audio_in_dir + "\\" + audio_in_name)
    audio_length = int(audio_length)
    epoch = audio_length / dur_time
    epoch = int(epoch)

    for i in range(epoch):
        audio_out_name = "%02d" % out_number + ".wav"   #切割完生成的片段名
        print(audio_out_name)
        audio_out_path = audio_out_dir + "/" + audio_out_name
        print(audio_out_path)
        audio_cut(audio_in_path, audio_out_path, start_time, dur_time)
        out_number = out_number + 1
        start_time = start_time + dur_time

    # 最后一个片段单独处理
    # 放在loop中比较麻烦
    if(epoch * dur_time != audio_length):
        audio_out_name = "%02d" % out_number + ".wav"  # 切割完生成的片段名
        print(audio_out_name)
        audio_out_path = audio_out_dir + "/" + audio_out_name
        print(audio_out_path)
        start_time = epoch * dur_time
        audio_cut(audio_in_path, audio_out_path, start_time, audio_length - start_time)


def fileProcess(audio_in_dir, audio_out_dir, audio_in_name):
    # audio_in_dir: 输入的文件的dir
    # audio_out_dir: 输出地址
    # audio_in_name:  要切割的文件名

    # audio_in_dir = r"D:\PycharmProject\Project_Degree_Demo\project\static\resource"
    # audio_out_dir = r"D:\PycharmProject\Project_Degree_Demo\project\static\temp\English"

    start_time = 0  # 切割开始时间
    dur_time = 30  # 切割的片段时长s
    out_number = 0  # 输出文件序号
    audio_in_path = audio_in_dir + "/" + audio_in_name
    audio_length = get_duration(audio_in_dir + "\\" + audio_in_name)
    audio_length = int(audio_length)
    epoch = audio_length / dur_time
    epoch = int(epoch)

    for i in range(epoch):
        audio_out_name = "%02d" % out_number + ".wav"  # 切割完生成的片段名
        print(audio_out_name)
        audio_out_path = audio_out_dir + "/" + audio_out_name
        print(audio_out_path)
        audio_cut(audio_in_path, audio_out_path, start_time, dur_time)
        out_number = out_number + 1
        start_time = start_time + dur_time

    # 最后一个片段单独处理
    # 放在loop中比较麻烦
    if (epoch * dur_time != audio_length):
        audio_out_name = "%02d" % out_number + ".wav"  # 切割完生成的片段名
        print(audio_out_name)
        audio_out_path = audio_out_dir + "/" + audio_out_name
        print(audio_out_path)
        start_time = epoch * dur_time
        audio_cut(audio_in_path, audio_out_path, start_time, audio_length - start_time)

# if __name__ == "__main__":
#     main()
    # getFrameRate('resource/test.wav')

# fileProcess(" ", " ", "test.wav")
