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
from django.conf.urls.i18n import i18n_patterns

# 语言切换URL
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# 使用i18n_patterns包装所有需要国际化的URL
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
    prefix_default_language=False,  # 不显示默认语言的前缀
)

# 添加静态文件和媒体文件的URL配置
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
