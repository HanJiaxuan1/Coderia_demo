from django.urls import path
from . import views

app_name = 'note'

urlpatterns = [
    path('video_note/', views.video_note, name='video_note'),
    path('code_note/', views.code_note, name='code_note'),
    path('show_notes/', views.show_notes, name='show_notes'),
    path('note_detail/<note_id>/', views.note_detail, name='note_detail'),
    path('save_comment/', views.save_comment, name = 'save_comment'),
    path('get_reply/', views.get_reply, name='get_reply'),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('code_editor/', views.code_editor, name='code_editor'),
]