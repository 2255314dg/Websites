from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Grade
from .forms import GradeForm, GradeSearchForm

class GradeListView(ListView):
    """成绩列表视图"""
    model = Grade
    template_name = 'grades/grade_list.html'
    context_object_name = 'grades'
    paginate_by = 10
    
    def get_queryset(self):
        """支持搜索功能"""
        queryset = super().get_queryset()
        form = GradeSearchForm(self.request.GET or None)
        
        if form.is_valid():
            student_id = form.cleaned_data.get('student_id')
            student_name = form.cleaned_data.get('student_name')
            course_code = form.cleaned_data.get('course_code')
            course_name = form.cleaned_data.get('course_name')
            semester = form.cleaned_data.get('semester')
            
            if student_id:
                queryset = queryset.filter(student__student_id__icontains=student_id)
            if student_name:
                queryset = queryset.filter(student__name__icontains=student_name)
            if course_code:
                queryset = queryset.filter(course__course_code__icontains=course_code)
            if course_name:
                queryset = queryset.filter(course__title__icontains=course_name)
            if semester:
                queryset = queryset.filter(semester=semester)
        
        return queryset.order_by('student', 'course', 'semester')
    
    def get_context_data(self, **kwargs):
        """添加搜索表单到上下文"""
        context = super().get_context_data(**kwargs)
        context['search_form'] = GradeSearchForm(self.request.GET or None)
        return context

class GradeDetailView(DetailView):
    """成绩详情视图"""
    model = Grade
    template_name = 'grades/grade_detail.html'
    context_object_name = 'grade'

class GradeCreateView(CreateView):
    """创建成绩记录视图"""
    model = Grade
    form_class = GradeForm
    template_name = 'grades/grade_form.html'
    success_url = reverse_lazy('grade_list')
    
    def form_valid(self, form):
        """保存前的额外处理"""
        return super().form_valid(form)

class GradeUpdateView(UpdateView):
    """更新成绩记录视图"""
    model = Grade
    form_class = GradeForm
    template_name = 'grades/grade_form.html'
    success_url = reverse_lazy('grade_list')
    
    def form_valid(self, form):
        """保存前的额外处理"""
        return super().form_valid(form)

class GradeDeleteView(DeleteView):
    """删除成绩记录视图"""
    model = Grade
    template_name = 'grades/grade_confirm_delete.html'
    success_url = reverse_lazy('grade_list')
