import os

basedir = os.path.abspath(os.path.dirname(__file__))

# video部分的参数
VIDEO_UPLOAD_DIR = os.path.join(basedir, 'static/video')
input_path = os.path.join(basedir, 'static/video')
output_path_Ch = os.path.join(basedir, 'static/video/temp/Chinese')
output_path_En = os.path.join(basedir, 'static/video/temp/English')

video_display_dir = "static/video"