from django.db import models
from students.models import Student
from courses.models import Course

class Grade(models.Model):
    SEMESTER_CHOICES = (
        ('2024-2025-1', '2024-2025学年第一学期'),
        ('2024-2025-2', '2024-2025学年第二学期'),
        ('2025-2026-1', '2025-2026学年第一学期'),
        ('2025-2026-2', '2025-2026学年第二学期'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学生')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    semester = models.CharField(max_length=15, choices=SEMESTER_CHOICES, default='2024-2025-1', verbose_name='学期')
    midterm_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='期中考试成绩')
    final_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='期末考试成绩')
    attendance_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='考勤成绩')
    assignment_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='作业成绩')
    project_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='项目成绩')
    total_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='总评成绩')
    grade_level = models.CharField(max_length=2, blank=True, null=True, verbose_name='等级')
    comments = models.TextField(blank=True, verbose_name='教师评语')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f'{self.student} - {self.course} - {self.semester}'
    
    def calculate_total_score(self):
        """计算总评成绩"""
        if self.final_score is not None:
            # 默认权重：期末考试60%，期中考试20%，考勤10%，作业10%
            total = self.final_score * 0.6
            if self.midterm_score is not None:
                total += self.midterm_score * 0.2
            if self.attendance_score is not None:
                total += self.attendance_score * 0.1
            if self.assignment_score is not None:
                total += self.assignment_score * 0.1
            return round(total, 2)
        return None
    
    def calculate_grade_level(self):
        """根据总评成绩计算等级"""
        if self.total_score is not None:
            if self.total_score >= 90:
                return 'A'
            elif self.total_score >= 80:
                return 'B'
            elif self.total_score >= 70:
                return 'C'
            elif self.total_score >= 60:
                return 'D'
            else:
                return 'F'
        return None
    
    def save(self, *args, **kwargs):
        """保存前自动计算总评成绩和等级"""
        self.total_score = self.calculate_total_score()
        self.grade_level = self.calculate_grade_level()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = '成绩'
        verbose_name_plural = '成绩管理'
        unique_together = ('student', 'course', 'semester')  # 确保每个学生每门课每学期只有一条成绩记录
        ordering = ['student', 'course', 'semester']
