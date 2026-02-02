from django.contrib import admin
from .models import Grade

class GradeAdmin(admin.ModelAdmin):
    """成绩管理后台配置"""
    list_display = [
        'student', 'course', 'semester', 
        'midterm_score', 'final_score', 'total_score', 'grade_level'
    ]
    list_filter = ['semester', 'course']
    search_fields = [
        'student__student_id', 'student__name', 
        'course__course_code', 'course__title'
    ]
    ordering = ['student', 'course', 'semester']
    date_hierarchy = 'created_at'
    readonly_fields = ['total_score', 'grade_level']
    fieldsets = (
        ('基本信息', {
            'fields': ('student', 'course', 'semester')
        }),
        ('成绩信息', {
            'fields': (
                'midterm_score', 'final_score', 'attendance_score', 
                'assignment_score', 'project_score', 'total_score', 'grade_level'
            )
        }),
        ('其他信息', {
            'fields': ('comments',)
        }),
    )

admin.site.register(Grade, GradeAdmin)
