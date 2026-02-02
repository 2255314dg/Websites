from django.db import models
from students.models import Student

class Teacher(models.Model):
    """教师模型"""
    teacher_id = models.CharField(max_length=20, unique=True, verbose_name='教师编号')
    name = models.CharField(max_length=100, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=[('male', '男'), ('female', '女')], verbose_name='性别')
    title = models.CharField(max_length=50, verbose_name='职称')
    department = models.CharField(max_length=100, verbose_name='所属部门')
    email = models.EmailField(max_length=100, verbose_name='邮箱')
    phone = models.CharField(max_length=20, verbose_name='电话')
    office = models.CharField(max_length=100, blank=True, null=True, verbose_name='办公室')
    bio = models.TextField(blank=True, null=True, verbose_name='个人简介')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f'{self.teacher_id} - {self.name}'

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师'

class Course(models.Model):
    """课程模型"""
    course_code = models.CharField(max_length=20, unique=True, verbose_name='课程代码')
    title = models.CharField(max_length=200, verbose_name='课程名称')
    description = models.TextField(blank=True, null=True, verbose_name='课程描述')
    credits = models.PositiveIntegerField(verbose_name='学分')
    # 添加教师关联
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='任课教师')
    # 添加课程类型
    course_type = models.CharField(max_length=20, choices=[('required', '必修课'), ('elective', '选修课')], default='required', verbose_name='课程类型')
    # 添加开课学期
    semester = models.CharField(max_length=20, default='2024-2025-1', verbose_name='开课学期')
    # 添加最大选课人数
    max_students = models.PositiveIntegerField(default=60, verbose_name='最大选课人数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f'{self.course_code} - {self.title}'

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'

class ClassSchedule(models.Model):
    """排课信息模型"""
    DAYS_OF_WEEK = [
        ('monday', '周一'),
        ('tuesday', '周二'),
        ('wednesday', '周三'),
        ('thursday', '周四'),
        ('friday', '周五'),
        ('saturday', '周六'),
        ('sunday', '周日'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK, verbose_name='星期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    classroom = models.CharField(max_length=50, verbose_name='教室')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f'{self.course.title} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}'

    class Meta:
        verbose_name = '排课信息'
        verbose_name_plural = '排课信息'

class Enrollment(models.Model):
    """学生选课模型"""
    SEMESTER_CHOICES = (
        ('2024-2025-1', '2024-2025学年第一学期'),
        ('2024-2025-2', '2024-2025学年第二学期'),
        ('2025-2026-1', '2025-2026学年第一学期'),
        ('2025-2026-2', '2025-2026学年第二学期'),
    )
    
    STATUS_CHOICES = (
        ('enrolled', '已选'),
        ('dropped', '已退课'),
        ('completed', '已完成'),
        ('in_progress', '进行中'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学生')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    semester = models.CharField(max_length=15, choices=SEMESTER_CHOICES, default='2024-2025-1', verbose_name='学期')
    enrollment_date = models.DateTimeField(auto_now_add=True, verbose_name='选课时间')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='enrolled', verbose_name='选课状态')
    
    def __str__(self):
        return f'{self.student} - {self.course} ({self.get_semester_display()})'
    
    class Meta:
        verbose_name = '选课记录'
        verbose_name_plural = '选课记录'
        # 确保每个学生在同一学期内不能重复选同一门课
        unique_together = ['student', 'course', 'semester']
