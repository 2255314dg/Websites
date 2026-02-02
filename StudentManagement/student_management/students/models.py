from django.db import models

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    )
    
    STATUS_CHOICES = (
        ('enrolled', '在读'),
        ('suspended', '休学'),
        ('graduated', '毕业'),
        ('dropped', '退学'),
    )
    
    POLITICAL_STATUS_CHOICES = (
        ('party_member', '党员'),
        ('probationary_member', '预备党员'),
        ('league_member', '团员'),
        ('mass', '群众'),
    )
    
    student_id = models.CharField(max_length=20, primary_key=True, verbose_name='学号')
    name = models.CharField(max_length=100, verbose_name='姓名')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='性别')
    date_of_birth = models.DateField(verbose_name='出生日期')
    ethnicity = models.CharField(max_length=50, default='汉族', verbose_name='民族')
    political_status = models.CharField(max_length=20, choices=POLITICAL_STATUS_CHOICES, default='mass', verbose_name='政治面貌')
    major = models.CharField(max_length=100, verbose_name='专业')
    class_name = models.CharField(max_length=50, default='未分配', verbose_name='班级')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    address = models.TextField(blank=True, verbose_name='家庭住址')
    emergency_contact = models.CharField(max_length=100, default='', verbose_name='紧急联系人')
    emergency_phone = models.CharField(max_length=20, default='', verbose_name='紧急联系电话')
    enrollment_date = models.DateField(verbose_name='入学日期')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled', verbose_name='学籍状态')
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True, verbose_name='照片')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f'{self.student_id} - {self.name}'
    
    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生管理'
        ordering = ['student_id']

# Create your models here.
