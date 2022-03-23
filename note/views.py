import json
import os
import random
import subprocess
import sys
import tempfile
import time

import settings as Config
from django.shortcuts import render, redirect
from note.API import file_convert, file_preprocessing, English, Chinese

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

# 创建临时文件夹,返回临时文件夹路径
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from werkzeug import Response

from note.models import Note, User, Video


def video_note(request):
    return render(request, 'codeEditor.html')


def code_note(request):
    if request.session['uid'] is None:
        return redirect(reverse('login'))
    return render(request, 'post.html')


def show_notes(request):
    note_list = Note.objects.all()
    return render(request, 'note_blog.html', {'note_list': note_list})


def note_detail(request, note_id):
    find_note = Note.objects.get(note_id=note_id)
    return render(request, 'note_detail.html', {'note': find_note})


def upload_video(request):
    # 测试
    request.session['uid'] = 1
    if request.method == "POST":
        path = Config.VIDEO_UPLOAD_DIR
        JudgePath(path)
        file = request.FILES.get("file")
        filename = file.name
        language = request.POST.get("language", 'None')
        mode = request.POST.get("mode", "None")
        if language is None:
            print("fail to upload video")
            return render(request, 'upload.html')
        # 没有file的保存方法，只能create一个file然后写入
        # 解决命名冲突
        check = Video.objects.filter(name=filename).first()
        while check is not None:
            num = random.randint(1, 10)
            filename = filename.split(".")[0] + str(num) + ".mp4"
            check = Video.objects.filter(name=filename).first()
        mp4 = open(os.path.join(path, filename), 'wb')
        for chunk in file.chunks():
            mp4.write(chunk)
        mp4.close()
        filename, text = VideoProcess(language, mode, filename, request.session.get('uid'))
        filename = os.path.join(Config.video_display_dir, filename)
        dic = {}
        dic['filename'] = filename
        dic['text'] = text
        return render(request, 'codeEditor.html', dic)

    return render(request, 'upload.html')

def VideoProcess(language, mode, filename, uid):
    pre_file = filename
    input_path = Config.input_path
    output_path_Ch = Config.output_path_Ch
    output_path_En = Config.output_path_En
    JudgePath(output_path_Ch)
    JudgePath(output_path_En)
    # MP4 -> Wav
    file_convert.MP4ToWav(input_path, input_path, filename)
    # delete this wav file
    # os.remove(os.path.join(input_path, filename))
    filename = filename.split('.')[0] + ".wav"
    while 1:
        judge = os.path.exists(os.path.join(input_path, filename))
        if judge:
            break
    # 如果马上使用这个wav,会有bug,因此先sleep 5s
    time.sleep(5)
    text = ""
    if language == 'English':
        file_preprocessing.fileProcess(input_path, output_path_En, filename)
        time.sleep(5)
        text = English.getText(output_path_En)
        # 缺联立uid来存储video
        video = Video(uid=uid, name=pre_file, text=text, language='English')
    elif language == 'Chinese':
        file_preprocessing.fileProcess(input_path, output_path_Ch, filename)
        time.sleep(5)
        text = Chinese.getText(output_path_Ch)
        video = Video(uid=uid, name=pre_file, text=text, language='Chinese')
    video.save()
    # 删除wav文件
    os.remove(os.path.join(Config.video_display_dir,filename))
    return filename, text


# 判断该目录是否存在，如果不存在则生成改目录
def JudgePath(path):
    if not os.path.exists(path):
        os.makedirs(path)


def code_editor(request):
    video = Video.objects.filter(vid = request.session.get('uid')).first()
    text = video.text
    filename = video.name
    filename = os.path.join(Config.video_display_dir, filename)
    dic = {}
    dic['filename'] = filename
    dic['text'] = text
    return render(request, 'codeEditor.html', dic)
