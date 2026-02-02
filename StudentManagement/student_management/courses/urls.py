from django.urls import path
from . import views

urlpatterns = [
    # 课程管理URL
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    
    # 教师管理URL
    path('teachers/', views.TeacherListView.as_view(), name='teacher_list'),
    path('teachers/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('teachers/create/', views.TeacherCreateView.as_view(), name='teacher_create'),
    path('teachers/<int:pk>/update/', views.TeacherUpdateView.as_view(), name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='teacher_delete'),
    
    # 排课管理URL
    path('schedules/', views.ClassScheduleListView.as_view(), name='schedule_list'),
    path('schedules/create/', views.ClassScheduleCreateView.as_view(), name='schedule_create'),
    path('schedules/<int:pk>/update/', views.ClassScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedules/<int:pk>/delete/', views.ClassScheduleDeleteView.as_view(), name='schedule_delete'),
]