from django import forms
from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = [
            'student', 'course', 'semester', 
            'midterm_score', 'final_score', 'attendance_score', 
            'assignment_score', 'project_score', 'comments'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'midterm_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'final_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'attendance_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'assignment_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'project_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }
        labels = {
            'student': '学生',
            'course': '课程',
            'semester': '学期',
            'midterm_score': '期中考试成绩',
            'final_score': '期末考试成绩',
            'attendance_score': '考勤成绩',
            'assignment_score': '作业成绩',
            'project_score': '项目成绩',
            'comments': '教师评语',
        }

class GradeSearchForm(forms.Form):
    """成绩查询表单"""
    student_id = forms.CharField(required=False, label='学号', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入学号'}))
    student_name = forms.CharField(required=False, label='姓名', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入姓名'}))
    course_code = forms.CharField(required=False, label='课程代码', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入课程代码'}))
    course_name = forms.CharField(required=False, label='课程名称', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入课程名称'}))
    semester = forms.ChoiceField(required=False, label='学期', choices=[('', '全部学期')] + list(Grade.SEMESTER_CHOICES), widget=forms.Select(attrs={'class': 'form-control'}))
