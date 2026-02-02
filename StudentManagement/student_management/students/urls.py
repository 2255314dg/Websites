from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentListView.as_view(), name='student-list'),
    path('<str:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('create/', views.StudentCreateView.as_view(), name='student-create'),
    path('<str:pk>/update/', views.StudentUpdateView.as_view(), name='student-update'),
    path('<str:pk>/delete/', views.StudentDeleteView.as_view(), name='student-delete'),
]