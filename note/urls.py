from django.urls import path
from . import views

app_name = 'note'

urlpatterns = [
    path('video_note/', views.video_note, name='video_note'),
    path('code_note/', views.code_note, name='code_note'),
    path('show_notes/', views.show_notes, name='show_notes'),
    path('note_detail/<note_id>/', views.note_detail, name='note_detail'),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('code_editor/', views.code_editor, name='code_editor'),
]