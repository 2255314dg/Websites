from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from students.models import Student
from courses.models import Teacher

class Profile(models.Model):
    # 用户类型选项
    USER_TYPE_CHOICES = (
        ('student', '学生'),
        ('teacher', '教师'),
        ('admin', '管理员'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # 关联学生或教师信息
    student = models.OneToOneField(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profile')
    teacher = models.OneToOneField(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.get_user_type_display()}'

# 当创建User时自动创建Profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# 当更新User时自动更新Profile
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
