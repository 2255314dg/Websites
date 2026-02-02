from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.urls import resolve

class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # 获取当前请求的URL名称
        url_name = resolve(request.path_info).url_name
        
        # 公开访问的URL列表
        public_urls = [
            'home', 'login', 'register', 'logout',
            'password_reset', 'password_reset_done', 'password_reset_confirm', 'password_reset_complete'
        ]
        
        # 如果URL是公开访问的，直接返回响应
        if url_name in public_urls:
            return self.get_response(request)
        
        # 如果用户未登录，重定向到登录页面
        if not request.user.is_authenticated:
            return redirect('login')
        
        # 获取用户类型
        user_type = request.user.profile.user_type
        
        # 学生可以访问的URL模式
        student_url_patterns = ['student_', 'course_list', 'grade_', 'enrollment_']
        
        # 教师可以访问的URL模式
        teacher_url_patterns = ['teacher_', 'course_', 'grade_', 'enrollment_']
        
        # 管理员可以访问的URL模式
        admin_url_patterns = ['admin:', 'student_', 'teacher_', 'course_', 'grade_', 'enrollment_', 'accounts_']
        
        # 检查用户权限
        if user_type == 'student':
            for pattern in student_url_patterns:
                if url_name.startswith(pattern):
                    return self.get_response(request)
        elif user_type == 'teacher':
            for pattern in teacher_url_patterns:
                if url_name.startswith(pattern):
                    return self.get_response(request)
        elif user_type == 'admin':
            for pattern in admin_url_patterns:
                if url_name.startswith(pattern) or url_name.startswith('admin:'):
                    return self.get_response(request)
        
        # 如果用户没有权限访问当前URL，返回403错误
        return HttpResponseForbidden("您没有权限访问该页面。")
