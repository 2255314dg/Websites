from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id', 'name', 'gender', 'date_of_birth', 'ethnicity',
            'political_status', 'major', 'class_name', 'email', 'phone',
            'address', 'emergency_contact', 'emergency_phone', 'enrollment_date',
            'status', 'photo'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
