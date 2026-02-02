#!/usr/bin/env python
"""
创建Django超级用户的脚本
使用方法：python create_superuser.py <username> <password> <email>
如果不提供参数，将使用默认值：admin / admin123 / admin@example.com
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_dashboard.settings")
django.setup()

from django.contrib.auth.models import User

def create_superuser(username='admin', password='admin123', email='admin@example.com'):
    """创建超级用户"""
    if User.objects.filter(username=username).exists():
        print(f"超级用户 '{username}' 已存在")
        return False
    
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"超级用户 '{username}' 创建成功")
    print("请在生产环境中立即更改密码！")
    return True

if __name__ == '__main__':
    # 解析命令行参数
    args = sys.argv[1:]
    if len(args) == 3:
        create_superuser(args[0], args[1], args[2])
    elif len(args) == 2:
        create_superuser(args[0], args[1])
    elif len(args) == 1:
        create_superuser(args[0])
    else:
        # 使用默认值
        print("使用默认参数创建超级用户：admin / admin123 / admin@example.com")
        print("生产环境请使用：python create_superuser.py <username> <password> <email>")
        create_superuser()
