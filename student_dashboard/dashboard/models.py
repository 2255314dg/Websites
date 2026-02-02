from django.db import models
from django.utils import timezone

class Student(models.Model):
    class_status_choices = [
        ('freshman', '大一'),
        ('sophomore', '大二'),
        ('junior', '大三'),
        ('senior', '大四'),
    ]
    major_choices = [
        ('computer', '计算机科学与技术'),
        ('electronics', '电子信息工程'),
        ('mechanical', '机械工程'),
        ('civil', '土木工程'),
        ('business', '工商管理'),
        ('medicine', '临床医学'),
    ]
    return_status_choices = [
        ('returned', '已返校'),
        ('not_returned', '未返校'),
        ('delayed', '延期返校'),
    ]
    return_method_choices = [
        ('train', '火车'),
        ('plane', '飞机'),
        ('bus', '汽车'),
        ('private_car', '私家车'),
        ('other', '其他'),
    ]
    
    student_id = models.CharField(max_length=12, unique=True, verbose_name='学号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=[('male', '男'), ('female', '女')], verbose_name='性别')
    class_status = models.CharField(max_length=20, choices=class_status_choices, verbose_name='年级')
    major = models.CharField(max_length=50, choices=major_choices, verbose_name='专业')
    return_status = models.CharField(max_length=20, choices=return_status_choices, verbose_name='返校状态')
    return_time = models.DateTimeField(null=True, blank=True, verbose_name='返校时间')
    return_method = models.CharField(max_length=20, choices=return_method_choices, null=True, blank=True, verbose_name='返校方式')
    contact = models.CharField(max_length=11, verbose_name='联系电话')
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.student_id} - {self.name}'
    
    class Meta:
        verbose_name = '学生返校信息'
        verbose_name_plural = '学生返校信息'
