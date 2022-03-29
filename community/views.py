import json
import os
import subprocess
import sys
import tempfile
import time

from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render, redirect
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from coderia.settings import MEDIA_ROOT
from note.models import User, Note, Category, UserCollectNote

TempFile = tempfile.mkdtemp(suffix='_test', prefix='python_')
# 文件名
FileNum = int(time.time() * 1000)
# python编译器位置
EXEC = sys.executable


def index(request):
    return render(request, 'index.html')


def about_us(request):
    return render(request, 'about-us.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def LoginCheck(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    find_user = User.objects.filter(username=username).first()
    if find_user is None or find_user.verify_password(password) is False:
        return HttpResponse("0")
    request.session["uid"] = find_user.uid
    return HttpResponse("1")


def RegisterCheck(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    find_user = User.objects.filter(username=username).first()
    if find_user is not None:
        return HttpResponse("0")
    password_hash = generate_password_hash(password)
    new_user = User(username=username,
                    password_hash=password_hash)
    new_user.save()
    return HttpResponse("1")


# 获取python版本
def get_version():
    v = sys.version_info
    version = "python %s.%s" % (v.major, v.minor)
    return version


# 获得py文件名
def get_pyname():
    global FileNum
    return 'test_%d' % FileNum


# 接收代码写入文件
def write_file(pyname, code):
    fpath = os.path.join(TempFile, '%s.py' % pyname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(code)
    print('file path: %s' % fpath)
    return fpath


# 编码
def decode(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return s.decode('gbk')

        # 主执行函数


def main(code):
    r = dict()
    r["version"] = get_version()
    pyname = get_pyname()
    fpath = write_file(pyname, code)
    try:
        # subprocess.check_output 是 父进程等待子进程完成，返回子进程向标准输出的输出结果
        # stderr是标准输出的类型
        outdata = decode(subprocess.check_output([EXEC, fpath], stderr=subprocess.STDOUT, timeout=10))
    except subprocess.CalledProcessError as e:
        # e.output是错误信息标准输出
        # 错误返回的数据
        r["code"] = 'Error'
        r["output"] = decode(e.output)
        return r
    else:
        # 成功返回的数据
        r['output'] = outdata
        r["code"] = "Success"
        return r
    finally:
        # 删除文件(其实不用删除临时文件会自动删除)
        try:
            os.remove(fpath)
        except Exception as e:
            exit(1)


def Response_headers(content):
    resp = HttpResponse(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp


def CompileCode(request):
    if request.method == 'POST' and request.POST.get('code'):
        code = request.POST.get('code')
        json_data = main(code)

        json_d = json.dumps(json_data)
        return Response_headers(str(json_d))


def PostNote(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        content_html = request.POST.get('content_html')
        category = Category.objects.get(name='python')
        if title is None:
            return HttpResponse("0")
        if content is None:
            return HttpResponse("1")
        user = User.objects.get(uid=request.session['uid'])
        new_note = Note(title=title, content=content, content_html=content_html, uid=user, category=category)
        new_note.save()
        return HttpResponse("2")


def NoteDetail(request):
    if request.method == 'POST':
        note_id = request.POST.get('note_id')
        find_note = Note.objects.get(note_id=note_id)
        if find_note is None:
            return HttpResponse("0")
        note_detail = {'note_id': find_note.note_id, 'title': find_note.title,
                       'content': find_note.content, 'content_html': find_note.content_html,
                       'timestamp': find_note.timestamp, 'user_id': find_note.uid.uid,
                       'username': find_note.uid.username}
        note_data = json.dumps(note_detail)
        return HttpResponse(note_data)


def profile(request):
    if 'uid' not in request.session.keys():
        return redirect(reverse('login'))
    user = User.objects.get(uid=request.session['uid'])
    my_note = Note.objects.filter(uid=request.session['uid']).all()
    collect_note = UserCollectNote.objects.filter(user_id=request.session['uid']).all()
    return render(request, 'profile.html', {'user': user, 'my_note': my_note, 'collect_note':collect_note})


def ModifyProfile(request):
    if 'uid' not in request.session.keys():
        return redirect(reverse('login'))
    user = User.objects.get(uid=request.session['uid'])
    if request.method == 'POST':
        username = request.POST.get('username')
        check_user = User.objects.filter(username=username).first()
        if check_user is None or user.uid == check_user.uid:
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            region = request.POST.get('region')
            phone = request.POST.get('phone')
            birthday = request.POST.get('birthday')
            email = request.POST.get('email')
            user.username = username
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.birthday = birthday
            user.region = region
            user.telephone = phone
            user.save()
            return HttpResponse(1)
    return HttpResponse(0)


def ChangeAvatar(request):
    if 'uid' not in request.session.keys():
        return redirect(reverse('login'))
    user = User.objects.get(uid=request.session['uid'])
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file and allow_file(file.name):
            local_path = MEDIA_ROOT + "\\" + file.name
            with open(local_path, 'wb') as pic:
                for c in file.chunks():
                    pic.write(c)
            user.avatar = file.name
            user.save()
            response = json.dumps(file.name)
            return HttpResponse(response)
    return HttpResponse(0)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}


def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def test(request):
    return render(request, 'test.html')


def DeleteNote(request):
    note_id = request.POST.get('note_id')
    note_delete = Note.objects.filter(note_id=note_id).first()
    if note_delete is not None:
        note_delete.delete()
        return HttpResponse(1)
    return HttpResponse(0)


def CancelCollectNote(request):
    if 'uid' not in request.session.keys():
        return redirect(reverse('login'))
    user = User.objects.get(uid=request.session['uid'])
    note_id = request.POST.get('note_id')
    note_collect = Note.objects.filter(note_id=note_id).first()
    if note_collect is not None:
        user.cancel_collect(note_collect)
        return HttpResponse(1)
    return HttpResponse(0)


def CollectNote(request):
    if 'uid' not in request.session.keys():
        return redirect(reverse('login'))
    user = User.objects.get(uid=request.session['uid'])
    note_id = request.POST.get('note_id')
    note_collect = Note.objects.filter(note_id=note_id).first()
    if note_collect is not None:
        user.collect(note_collect)
        return HttpResponse(1)
    return HttpResponse(0)


def CancelLikeNote(request):
    if 'uid' not in request.session.keys():
        return redirect(reverse('login'))
    user = User.objects.get(uid=request.session['uid'])
    note_id = request.POST.get('note_id')
    note_like = Note.objects.filter(note_id=note_id).first()
    if note_like is not None:
        user.cancel_like(note_like)
        return HttpResponse(1)
    return HttpResponse(0)


def LikeNote(request):
    if 'uid' not in request.session.keys():
        return redirect(reverse('login'))
    user = User.objects.get(uid=request.session['uid'])
    note_id = request.POST.get('note_id')
    note_like = Note.objects.filter(note_id=note_id).first()
    if note_like is not None:
        user.like(note_like)
        return HttpResponse(1)
    return HttpResponse(0)

