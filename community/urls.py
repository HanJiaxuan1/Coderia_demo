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
    path('profile/', views.profile, name='profile'),
    path('ModifyProfile/', views.ModifyProfile, name='ModifyProfile'),
    path('test/', views.test, name='test'),
    path('ChangeAvatar/', views.ChangeAvatar, name='ChangeAvatar'),
    path('DeleteNote/', views.DeleteNote, name='DeleteNote'),
    path('CollectNote/', views.CollectNote, name='CollectNote'),
    path('CancelCollectNote/', views.CancelCollectNote, name='CancelCollectNote'),
    path('LikeNote/', views.LikeNote, name='LikeNote'),
    path('CancelLikeNote/', views.CancelLikeNote, name='CancelLikeNote'),
]