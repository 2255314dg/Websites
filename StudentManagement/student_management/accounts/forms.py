from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='请输入有效的邮箱地址')
    first_name = forms.CharField(max_length=30, required=True, help_text='请输入您的姓名')
    last_name = forms.CharField(max_length=30, required=False, help_text='可选')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
