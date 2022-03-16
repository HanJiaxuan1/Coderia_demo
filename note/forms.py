from django import forms
from django.contrib.auth.models import User

# 帖子编辑的表单设计
class PostMdForm(forms.ModelForm):
    body = forms.Textarea("Body")
    body_html = forms.HiddenInput()
