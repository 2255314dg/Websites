from django.urls import path
from . import views

"""
portfolio应用的URL路由配置

定义了应用的所有路由，包括首页、关于我、作品集、联系方式和项目详情页面。
"""
urlpatterns = [
    # 首页路由
    path('', views.home, name='home'),
    
    # 关于我页面路由
    path('about/', views.about, name='about'),
    
    # 作品集页面路由
    path('portfolio/', views.portfolio, name='portfolio'),
    
    # 视频页面路由
    path('portfolio/video/', views.video, name='video'),
    
    # 联系方式页面路由
    path('contact/', views.contact, name='contact'),
    
    # 项目详情页面路由，接收项目的slug作为参数
    path('portfolio/<slug:project_slug>/', views.project_detail, name='project_detail'),
]
