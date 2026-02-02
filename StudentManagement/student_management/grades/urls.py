from django.urls import path
from .views import (
    GradeListView,
    GradeDetailView,
    GradeCreateView,
    GradeUpdateView,
    GradeDeleteView
)

urlpatterns = [
    # 成绩列表和搜索
    path('', GradeListView.as_view(), name='grade_list'),
    # 成绩详情
    path('<int:pk>/', GradeDetailView.as_view(), name='grade_detail'),
    # 添加成绩
    path('add/', GradeCreateView.as_view(), name='grade_create'),
    # 更新成绩
    path('<int:pk>/edit/', GradeUpdateView.as_view(), name='grade_update'),
    # 删除成绩
    path('<int:pk>/delete/', GradeDeleteView.as_view(), name='grade_delete'),
]
