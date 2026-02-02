from django import forms
from .models import Course, ClassSchedule, Teacher


class TeacherForm(forms.ModelForm):
    """教师信息表单"""
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'name', 'gender', 'email', 'phone', 'department', 'title', 'office', 'bio']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'teacher_id': forms.TextInput(attrs={'class': 'form-control'}),
            'office': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'teacher_id': '教师编号',
            'name': '姓名',
            'gender': '性别',
            'email': '邮箱',
            'phone': '电话',
            'department': '部门',
            'title': '职称',
            'office': '办公室',
            'bio': '个人简介',
        }


class CourseForm(forms.ModelForm):
    """课程信息表单"""
    class Meta:
        model = Course
        fields = ['course_code', 'title', 'description', 'credits', 'teacher', 'course_type', 'semester', 'max_students']
        widgets = {
            'course_code': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'course_type': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.TextInput(attrs={'class': 'form-control'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'course_code': '课程代码',
            'title': '课程名称',
            'description': '课程描述',
            'credits': '学分',
            'teacher': '任课教师',
            'course_type': '课程类型',
            'semester': '开课学期',
            'max_students': '最大选课人数',
        }


class ClassScheduleForm(forms.ModelForm):
    """课程排课表单"""
    class Meta:
        model = ClassSchedule
        fields = ['course', 'day_of_week', 'start_time', 'end_time', 'classroom']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type': 'time'}),
            'classroom': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'course': '课程',
            'day_of_week': '星期',
            'start_time': '开始时间',
            'end_time': '结束时间',
            'classroom': '教室',
        }
