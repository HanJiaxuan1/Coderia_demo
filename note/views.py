import json
import os
import subprocess
import sys
import tempfile
import time

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

# 创建临时文件夹,返回临时文件夹路径
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from werkzeug import Response

from note.models import Note, User


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
    return render(request, 'upload.html')
