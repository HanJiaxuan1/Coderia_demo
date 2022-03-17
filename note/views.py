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




