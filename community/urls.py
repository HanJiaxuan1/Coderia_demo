from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('about-us/', views.about_us, name='about_us'),
    path('register/', views.register, name='register'),
    path('RegisterCheck/', views.RegisterCheck, name='RegisterCheck'),
    path('LoginCheck/', views.LoginCheck, name='LoginCheck'),
    path('CompileCode/', views.CompileCode, name='CompileCode'),
    path('PostNote/', views.PostNote, name='PostNote'),
    path('NoteDetail/', views.NoteDetail, name='NoteDetail'),
]