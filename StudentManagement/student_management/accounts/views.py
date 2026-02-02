from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

# 用户注册
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账户创建成功！欢迎 {username}')
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# 用户登录
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'登录成功！欢迎回来，{username}')
                return redirect('home')
            else:
                messages.error(request, '登录失败，请检查用户名和密码')
        else:
            messages.error(request, '登录失败，请检查用户名和密码')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# 用户注销
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, '已成功注销')
    return redirect('home')

# 个人资料页面
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
