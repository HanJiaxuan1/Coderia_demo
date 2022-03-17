from django.urls import path
from . import views

app_name = 'note'

urlpatterns = [
    path('video_note/', views.video_note, name='video_note'),
    path('code_note/', views.code_note, name='code_note'),
]