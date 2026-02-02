from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course, Teacher, ClassSchedule
from .forms import CourseForm, TeacherForm, ClassScheduleForm


# 课程管理视图
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 添加该课程的排课信息
        context['schedules'] = ClassSchedule.objects.filter(course=self.object)
        return context


class CourseCreateView(CreateView):
    model = Course
    template_name = 'courses/course_form.html'
    form_class = CourseForm
    success_url = reverse_lazy('course_list')


class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'courses/course_form.html'
    form_class = CourseForm
    success_url = reverse_lazy('course_list')


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')


# 教师管理视图
class TeacherListView(ListView):
    model = Teacher
    template_name = 'courses/teacher_list.html'
    context_object_name = 'teachers'


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'courses/teacher_detail.html'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 添加该教师教授的课程
        context['courses'] = Course.objects.filter(teacher=self.object)
        return context


class TeacherCreateView(CreateView):
    model = Teacher
    template_name = 'courses/teacher_form.html'
    form_class = TeacherForm
    success_url = reverse_lazy('teacher_list')


class TeacherUpdateView(UpdateView):
    model = Teacher
    template_name = 'courses/teacher_form.html'
    form_class = TeacherForm
    success_url = reverse_lazy('teacher_list')


class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'courses/teacher_confirm_delete.html'
    success_url = reverse_lazy('teacher_list')


# 排课管理视图
class ClassScheduleListView(ListView):
    model = ClassSchedule
    template_name = 'courses/schedule_list.html'
    context_object_name = 'schedules'


class ClassScheduleCreateView(CreateView):
    model = ClassSchedule
    template_name = 'courses/schedule_form.html'
    form_class = ClassScheduleForm
    success_url = reverse_lazy('schedule_list')


class ClassScheduleUpdateView(UpdateView):
    model = ClassSchedule
    template_name = 'courses/schedule_form.html'
    form_class = ClassScheduleForm
    success_url = reverse_lazy('schedule_list')


class ClassScheduleDeleteView(DeleteView):
    model = ClassSchedule
    template_name = 'courses/schedule_confirm_delete.html'
    success_url = reverse_lazy('schedule_list')
