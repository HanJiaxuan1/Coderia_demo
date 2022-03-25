from moviepy.editor import AudioFileClip
from aip import AipSpeech
import os
import wave
import ffmpeg

# reference: https://blog.csdn.net/qq_15821487/article/details/119206606?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164601479416780271539224%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=164601479416780271539224&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-1-119206606.pc_search_result_control_group&utm_term=%E5%A6%82%E4%BD%95%E8%B0%83%E7%94%A8%E7%99%BE%E5%BA%A6API%E5%AE%9E%E7%8E%B0%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB&spm=1018.2226.3001.4187

# load the video
# my_audio_clip = AudioFileClip("C:\\Users\\OMEN6\\Desktop\\test.mp4")
# extract the audio from the video and save
# my_audio_clip.write_audiofile("C:\\Users\\OMEN6\\Desktop\\test.wav")
# settings for Baidu API

APP_ID = '25675270'
API_KEY = 'tHeRjGj1yHywf4UxfGY6jKQV'
SECRET_KEY = 'H4YyTo0wd66mSgEOUk47cPd4w5I8TV1N'
# build the model
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
# read the file
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()

def deleteFiles(path):
    ls = os.listdir(path)
    for i in ls:
        f_path = os.path.join(path,i)
        # 判断是否是一个目录，若是则递归删除
        if os.path.isdir(f_path):
            deleteFiles(f_path)
        else:
            os.remove(f_path)

# identify the file and return the results
def getText(path):
    text = ""
    files = os.listdir(path)
    file_list = [path + '\\' + f for f in files if f.endswith('.wav')]
    for file in file_list:
        result = client.asr(get_file_content(file), 'wav', 16000, {
            'dev_pid': 1737,  # id 1737 for English to test the code
        })
        text += result['result'][0] + " "
    deleteFiles(path)
    return text

# getText('../static/temp/English')



