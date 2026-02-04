"""
URL configuration for profile_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# URL配置
urlpatterns = [
    # 后台管理URL
    path('admin/', admin.site.urls),
    
    # 包含portfolio应用的URL配置
    # 这样所有portfolio应用的路由都会被包含到项目的根URL中
    path('', include('portfolio.urls')),
]

# 添加静态文件和媒体文件的URL配置
# 仅在DEBUG模式下生效，用于开发环境
if settings.DEBUG:
    # 媒体文件的URL配置，用于访问上传的文件
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
