from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Student
import json
import csv
import xlwt
import xlrd
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os

@login_required
@cache_page(300)  # 缓存5分钟
def dashboard(request):
    # 统计总学生数
    total_students = Student.objects.count()
    
    # 按返校状态统计
    return_status_count = Student.objects.values('return_status').annotate(count=Count('id'))
    return_status_data = {
        'returned': 0,
        'not_returned': 0,
        'delayed': 0
    }
    for item in return_status_count:
        return_status_data[item['return_status']] = item['count']
    
    # 优化：按年级统计返校情况 - 使用单个查询替代三个独立查询
    class_status_stats = Student.objects.values('class_status').annotate(
        returned=Count('id', filter=Q(return_status='returned')),
        not_returned=Count('id', filter=Q(return_status='not_returned')),
        delayed=Count('id', filter=Q(return_status='delayed'))
    )
    
    class_status_data = {
        'labels': ['大一', '大二', '大三', '大四'],
        'returned': [0, 0, 0, 0],
        'not_returned': [0, 0, 0, 0],
        'delayed': [0, 0, 0, 0]
    }
    
    class_map = {'freshman': 0, 'sophomore': 1, 'junior': 2, 'senior': 3}
    for item in class_status_stats:
        if item['class_status'] in class_map:
            idx = class_map[item['class_status']]
            class_status_data['returned'][idx] = item['returned']
            class_status_data['not_returned'][idx] = item['not_returned']
            class_status_data['delayed'][idx] = item['delayed']
    
    # 按专业统计返校情况
    major_count = Student.objects.values('major').annotate(
        total=Count('id'),
        returned=Count('id', filter=Q(return_status='returned')),
        not_returned=Count('id', filter=Q(return_status='not_returned')),
        delayed=Count('id', filter=Q(return_status='delayed'))
    )
    
    major_data = {
        'labels': [],
        'returned': [],
        'not_returned': [],
        'delayed': []
    }
    
    major_map = {
        'computer': '计算机科学与技术',
        'electronics': '电子信息工程',
        'mechanical': '机械工程',
        'civil': '土木工程',
        'business': '工商管理',
        'medicine': '临床医学'
    }
    
    for item in major_count:
        major_data['labels'].append(major_map.get(item['major'], item['major']))
        major_data['returned'].append(item['returned'])
        major_data['not_returned'].append(item['not_returned'])
        major_data['delayed'].append(item['delayed'])
    
    # 按返校方式统计
    return_method_count = Student.objects.filter(return_status='returned').values('return_method').annotate(count=Count('id'))
    return_method_data = {
        'labels': ['火车', '飞机', '汽车', '私家车', '其他'],
        'data': [0, 0, 0, 0, 0]
    }
    
    method_map = {'train': 0, 'plane': 1, 'bus': 2, 'private_car': 3, 'other': 4}
    for item in return_method_count:
        if item['return_method'] in method_map:
            return_method_data['data'][method_map[item['return_method']]] = item['count']
    
    # 最近7天返校趋势
    today = timezone.now().date()
    date_range = [today - timezone.timedelta(days=i) for i in range(6, -1, -1)]
    daily_return_data = {
        'labels': [date.strftime('%Y-%m-%d') for date in date_range],
        'data': [0] * 7
    }
    
    recent_returns = Student.objects.filter(
        return_status='returned',
        return_time__date__range=[date_range[0], date_range[-1]]
    ).values('return_time__date').annotate(count=Count('id'))
    
    for item in recent_returns:
        date_str = item['return_time__date'].strftime('%Y-%m-%d')
        if date_str in daily_return_data['labels']:
            index = daily_return_data['labels'].index(date_str)
            daily_return_data['data'][index] = item['count']
    
    # 新增：性别分布统计
    gender_stats = Student.objects.values('gender').annotate(count=Count('id'))
    gender_data = {
        'male': 0,
        'female': 0
    }
    for item in gender_stats:
        gender_data[item['gender']] = item['count']
    
    # 新增：计算返校率
    returned_count = return_status_data['returned']
    return_rate = round((returned_count / total_students) * 100, 2) if total_students > 0 else 0
    not_return_rate = round((return_status_data['not_returned'] / total_students) * 100, 2) if total_students > 0 else 0
    delayed_rate = round((return_status_data['delayed'] / total_students) * 100, 2) if total_students > 0 else 0
    
    # 新增：按专业返校率排名
    major_return_rate = Student.objects.values('major').annotate(
        total=Count('id'),
        returned=Count('id', filter=Q(return_status='returned'))
    )
    
    major_return_rate_data = {
        'labels': [],
        'rates': [],
        'total': [],
        'returned': []
    }
    
    for item in major_return_rate:
        rate = round((item['returned'] / item['total']) * 100, 2) if item['total'] > 0 else 0
        major_return_rate_data['labels'].append(major_map.get(item['major'], item['major']))
        major_return_rate_data['rates'].append(rate)
        major_return_rate_data['total'].append(item['total'])
        major_return_rate_data['returned'].append(item['returned'])
    
    # 按返校率排序
    sorted_major_data = sorted(zip(major_return_rate_data['labels'], major_return_rate_data['rates'], major_return_rate_data['total'], major_return_rate_data['returned']), key=lambda x: x[1], reverse=True)
    if sorted_major_data:
        major_return_rate_data['labels'], major_return_rate_data['rates'], major_return_rate_data['total'], major_return_rate_data['returned'] = zip(*sorted_major_data)
    
    # 新增：按年级返校率排名
    class_return_rate = Student.objects.values('class_status').annotate(
        total=Count('id'),
        returned=Count('id', filter=Q(return_status='returned'))
    )
    
    class_return_rate_data = {
        'labels': ['大一', '大二', '大三', '大四'],
        'rates': [0, 0, 0, 0],
        'total': [0, 0, 0, 0],
        'returned': [0, 0, 0, 0]
    }
    
    class_map = {'freshman': 0, 'sophomore': 1, 'junior': 2, 'senior': 3}
    for item in class_return_rate:
        if item['class_status'] in class_map:
            idx = class_map[item['class_status']]
            class_return_rate_data['total'][idx] = item['total']
            class_return_rate_data['returned'][idx] = item['returned']
            class_return_rate_data['rates'][idx] = round((item['returned'] / item['total']) * 100, 2) if item['total'] > 0 else 0
    
    # 新增：性别与返校状态交叉分析数据
    gender_return_status_stats = Student.objects.values('gender', 'return_status').annotate(count=Count('id'))
    gender_return_status_data = {
        'male': {'returned': 0, 'not_returned': 0, 'delayed': 0},
        'female': {'returned': 0, 'not_returned': 0, 'delayed': 0}
    }
    for item in gender_return_status_stats:
        gender = item['gender']
        status = item['return_status']
        gender_return_status_data[gender][status] = item['count']
    
    # 新增：返校时间分布数据
    # 使用SQLite兼容的strftime函数替代PostgreSQL的EXTRACT
    return_time_stats = Student.objects.filter(return_status='returned').extra({
        'hour_range': "CASE "
                    "WHEN CAST(strftime('%%H', return_time) AS INTEGER) BETWEEN 0 AND 4 THEN '00:00-04:00' "
                    "WHEN CAST(strftime('%%H', return_time) AS INTEGER) BETWEEN 4 AND 8 THEN '04:00-08:00' "
                    "WHEN CAST(strftime('%%H', return_time) AS INTEGER) BETWEEN 8 AND 12 THEN '08:00-12:00' "
                    "WHEN CAST(strftime('%%H', return_time) AS INTEGER) BETWEEN 12 AND 16 THEN '12:00-16:00' "
                    "WHEN CAST(strftime('%%H', return_time) AS INTEGER) BETWEEN 16 AND 20 THEN '16:00-20:00' "
                    "ELSE '20:00-24:00' END"
    }).values('hour_range').annotate(count=Count('id'))
    
    return_time_distribution_data = {
        'labels': ['00:00-04:00', '04:00-08:00', '08:00-12:00', '12:00-16:00', '16:00-20:00', '20:00-24:00'],
        'data': [0, 0, 0, 0, 0, 0]
    }
    
    for item in return_time_stats:
        if item['hour_range'] in return_time_distribution_data['labels']:
            index = return_time_distribution_data['labels'].index(item['hour_range'])
            return_time_distribution_data['data'][index] = item['count']
    
    # 新增：各年级各专业返校率对比数据
    class_major_stats = Student.objects.values('class_status', 'major').annotate(
        total=Count('id'),
        returned=Count('id', filter=Q(return_status='returned'))
    )
    
    major_map = {
        'computer': '计算机科学与技术',
        'electronics': '电子信息工程',
        'mechanical': '机械工程',
        'civil': '土木工程',
        'business': '工商管理',
        'medicine': '临床医学'
    }
    
    unique_majors = list(major_map.values())
    class_major_return_rate_data = {
        'class_labels': ['大一', '大二', '大三', '大四'],
        'major_labels': unique_majors,
        'data': [[0 for _ in range(4)] for _ in range(len(unique_majors))]
    }
    
    for item in class_major_stats:
        major_name = major_map.get(item['major'], item['major'])
        if major_name in unique_majors:
            major_idx = unique_majors.index(major_name)
            if item['class_status'] in class_map:
                class_idx = class_map[item['class_status']]
                rate = round((item['returned'] / item['total']) * 100, 2) if item['total'] > 0 else 0
                class_major_return_rate_data['data'][major_idx][class_idx] = rate
    
    # 新增：返校方式与年级交叉分析数据
    method_class_stats = Student.objects.filter(return_status='returned').values('class_status', 'return_method').annotate(count=Count('id'))
    
    method_map = {'train': '火车', 'plane': '飞机', 'bus': '汽车', 'private_car': '私家车', 'other': '其他'}
    
    method_class_data = {
        'class_labels': ['大一', '大二', '大三', '大四'],
        'method_labels': ['火车', '飞机', '汽车', '私家车', '其他'],
        'data': [[0 for _ in range(4)] for _ in range(5)]
    }
    
    for item in method_class_stats:
        method_name = method_map.get(item['return_method'], item['return_method'])
        if method_name in method_class_data['method_labels']:
            method_idx = method_class_data['method_labels'].index(method_name)
            if item['class_status'] in class_map:
                class_idx = class_map[item['class_status']]
                method_class_data['data'][method_idx][class_idx] = item['count']
    
    context = {
        'total_students': total_students,
        'return_status_data': json.dumps(return_status_data),
        'class_status_data': json.dumps(class_status_data),
        'major_data': json.dumps(major_data),
        'return_method_data': json.dumps(return_method_data),
        'daily_return_data': json.dumps(daily_return_data),
        'gender_data': json.dumps(gender_data),
        'return_rate': return_rate,
        'not_return_rate': not_return_rate,
        'delayed_rate': delayed_rate,
        'major_return_rate_data': json.dumps(major_return_rate_data),
        'class_return_rate_data': json.dumps(class_return_rate_data),
        'gender_return_status_data': json.dumps(gender_return_status_data),
        'return_time_distribution_data': json.dumps(return_time_distribution_data),
        'class_major_return_rate_data': json.dumps(class_major_return_rate_data),
        'method_class_data': json.dumps(method_class_data),
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def dashboard_data(request):
    """返回JSON格式的仪表盘数据，支持筛选参数"""
    # 获取筛选参数
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    class_status = request.GET.getlist('class_status')
    major = request.GET.getlist('major')
    return_status = request.GET.getlist('return_status')
    
    # 构建查询集
    queryset = Student.objects.all()
    
    # 应用日期范围筛选
    if start_date and end_date:
        queryset = queryset.filter(return_time__date__range=[start_date, end_date])
    elif start_date:
        queryset = queryset.filter(return_time__date__gte=start_date)
    elif end_date:
        queryset = queryset.filter(return_time__date__lte=end_date)
    
    # 应用年级筛选
    if class_status:
        queryset = queryset.filter(class_status__in=class_status)
    
    # 应用专业筛选
    if major:
        queryset = queryset.filter(major__in=major)
    
    # 应用返校状态筛选
    if return_status:
        queryset = queryset.filter(return_status__in=return_status)
    
    # 统计总学生数
    total_students = queryset.count()
    
    # 按返校状态统计
    return_status_count = queryset.values('return_status').annotate(count=Count('id'))
    return_status_data = {
        'returned': 0,
        'not_returned': 0,
        'delayed': 0
    }
    for item in return_status_count:
        return_status_data[item['return_status']] = item['count']
    
    # 按年级统计返校情况
    class_status_stats = queryset.values('class_status').annotate(
        returned=Count('id', filter=Q(return_status='returned')),
        not_returned=Count('id', filter=Q(return_status='not_returned')),
        delayed=Count('id', filter=Q(return_status='delayed'))
    )
    
    class_status_data = {
        'labels': ['大一', '大二', '大三', '大四'],
        'returned': [0, 0, 0, 0],
        'not_returned': [0, 0, 0, 0],
        'delayed': [0, 0, 0, 0]
    }
    
    class_map = {'freshman': 0, 'sophomore': 1, 'junior': 2, 'senior': 3}
    for item in class_status_stats:
        if item['class_status'] in class_map:
            idx = class_map[item['class_status']]
            class_status_data['returned'][idx] = item['returned']
            class_status_data['not_returned'][idx] = item['not_returned']
            class_status_data['delayed'][idx] = item['delayed']
    
    # 按专业统计返校情况
    major_count = queryset.values('major').annotate(
        total=Count('id'),
        returned=Count('id', filter=Q(return_status='returned')),
        not_returned=Count('id', filter=Q(return_status='not_returned')),
        delayed=Count('id', filter=Q(return_status='delayed'))
    )
    
    major_data = {
        'labels': [],
        'returned': [],
        'not_returned': [],
        'delayed': []
    }
    
    major_map = {
        'computer': '计算机科学与技术',
        'electronics': '电子信息工程',
        'mechanical': '机械工程',
        'civil': '土木工程',
        'business': '工商管理',
        'medicine': '临床医学'
    }
    
    for item in major_count:
        major_data['labels'].append(major_map.get(item['major'], item['major']))
        major_data['returned'].append(item['returned'])
        major_data['not_returned'].append(item['not_returned'])
        major_data['delayed'].append(item['delayed'])
    
    # 按返校方式统计
    return_method_queryset = queryset.filter(return_status='returned')
    return_method_count = return_method_queryset.values('return_method').annotate(count=Count('id'))
    return_method_data = {
        'labels': ['火车', '飞机', '汽车', '私家车', '其他'],
        'data': [0, 0, 0, 0, 0]
    }
    
    method_map = {'train': 0, 'plane': 1, 'bus': 2, 'private_car': 3, 'other': 4}
    for item in return_method_count:
        if item['return_method'] in method_map:
            return_method_data['data'][method_map[item['return_method']]] = item['count']
    
    # 最近7天返校趋势
    today = timezone.now().date()
    date_range = [today - timezone.timedelta(days=i) for i in range(6, -1, -1)]
    daily_return_data = {
        'labels': [date.strftime('%Y-%m-%d') for date in date_range],
        'data': [0] * 7
    }
    
    # 应用筛选后的最近返校数据
    recent_returns_queryset = queryset.filter(
        return_status='returned',
        return_time__date__range=[date_range[0], date_range[-1]]
    )
    recent_returns = recent_returns_queryset.values('return_time__date').annotate(count=Count('id'))
    
    for item in recent_returns:
        date_str = item['return_time__date'].strftime('%Y-%m-%d')
        if date_str in daily_return_data['labels']:
            index = daily_return_data['labels'].index(date_str)
            daily_return_data['data'][index] = item['count']
    
    # 新增：性别分布统计
    gender_stats = queryset.values('gender').annotate(count=Count('id'))
    gender_data = {
        'male': 0,
        'female': 0
    }
    for item in gender_stats:
        gender_data[item['gender']] = item['count']
    
    # 新增：计算返校率
    returned_count = return_status_data['returned']
    return_rate = round((returned_count / total_students) * 100, 2) if total_students > 0 else 0
    not_return_rate = round((return_status_data['not_returned'] / total_students) * 100, 2) if total_students > 0 else 0
    delayed_rate = round((return_status_data['delayed'] / total_students) * 100, 2) if total_students > 0 else 0
    
    # 新增：专业映射
    major_map = {
        'computer': '计算机科学与技术',
        'electronics': '电子信息工程',
        'mechanical': '机械工程',
        'civil': '土木工程',
        'business': '工商管理',
        'medicine': '临床医学'
    }
    
    # 新增：按专业返校率排名
    major_return_rate = queryset.values('major').annotate(
        total=Count('id'),
        returned=Count('id', filter=Q(return_status='returned'))
    )
    
    major_return_rate_data = {
        'labels': [],
        'rates': [],
        'total': [],
        'returned': []
    }
    
    for item in major_return_rate:
        rate = round((item['returned'] / item['total']) * 100, 2) if item['total'] > 0 else 0
        major_return_rate_data['labels'].append(major_map.get(item['major'], item['major']))
        major_return_rate_data['rates'].append(rate)
        major_return_rate_data['total'].append(item['total'])
        major_return_rate_data['returned'].append(item['returned'])
    
    # 按返校率排序
    sorted_major_data = sorted(zip(major_return_rate_data['labels'], major_return_rate_data['rates'], major_return_rate_data['total'], major_return_rate_data['returned']), key=lambda x: x[1], reverse=True)
    if sorted_major_data:
        major_return_rate_data['labels'], major_return_rate_data['rates'], major_return_rate_data['total'], major_return_rate_data['returned'] = zip(*sorted_major_data)
    
    # 新增：按年级返校率排名
    class_return_rate = queryset.values('class_status').annotate(
        total=Count('id'),
        returned=Count('id', filter=Q(return_status='returned'))
    )
    
    class_return_rate_data = {
        'labels': ['大一', '大二', '大三', '大四'],
        'rates': [0, 0, 0, 0],
        'total': [0, 0, 0, 0],
        'returned': [0, 0, 0, 0]
    }
    
    class_map = {'freshman': 0, 'sophomore': 1, 'junior': 2, 'senior': 3}
    for item in class_return_rate:
        if item['class_status'] in class_map:
            idx = class_map[item['class_status']]
            class_return_rate_data['total'][idx] = item['total']
            class_return_rate_data['returned'][idx] = item['returned']
            class_return_rate_data['rates'][idx] = round((item['returned'] / item['total']) * 100, 2) if item['total'] > 0 else 0
    
    # 新增：性别与返校状态交叉分析数据
    gender_return_status_stats = queryset.values('gender', 'return_status').annotate(count=Count('id'))
    gender_return_status_data = {
        'male': {'returned': 0, 'not_returned': 0, 'delayed': 0},
        'female': {'returned': 0, 'not_returned': 0, 'delayed': 0}
    }
    for item in gender_return_status_stats:
        gender = item['gender']
        status = item['return_status']
        gender_return_status_data[gender][status] = item['count']
    
    # 新增：返校时间分布数据
    returned_queryset = queryset.filter(return_status='returned')
    # 使用SQLite兼容的strftime函数替代PostgreSQL的EXTRACT
    return_time_stats = returned_queryset.extra({
        'hour_range': "CASE "
                    "WHEN CAST(strftime('%%H', return_time) AS INTEGER) BETWEEN 0 AND 4 THEN '00:00-04:00' "
                    "WHEN CAST(strftime('%%H', return_time) AS INTEGER) BETWEEN 4 AND 8 THEN '04:00-08:00' "
                    "WHEN CAST(strftime('%%H', return_time) AS INTEGER) BETWEEN 8 AND 12 THEN '08:00-12:00' "
                    "WHEN CAST(strftime('%%H', return_time) AS INTEGER) BETWEEN 12 AND 16 THEN '12:00-16:00' "
                    "WHEN CAST(strftime('%%H', return_time) AS INTEGER) BETWEEN 16 AND 20 THEN '16:00-20:00' "
                    "ELSE '20:00-24:00' END"
    }).values('hour_range').annotate(count=Count('id'))
    
    return_time_distribution_data = {
        'labels': ['00:00-04:00', '04:00-08:00', '08:00-12:00', '12:00-16:00', '16:00-20:00', '20:00-24:00'],
        'data': [0, 0, 0, 0, 0, 0]
    }
    
    for item in return_time_stats:
        if item['hour_range'] in return_time_distribution_data['labels']:
            index = return_time_distribution_data['labels'].index(item['hour_range'])
            return_time_distribution_data['data'][index] = item['count']
    
    # 新增：各年级各专业返校率对比数据
    class_major_stats = queryset.values('class_status', 'major').annotate(
        total=Count('id'),
        returned=Count('id', filter=Q(return_status='returned'))
    )
    
    major_map = {
        'computer': '计算机科学与技术',
        'electronics': '电子信息工程',
        'mechanical': '机械工程',
        'civil': '土木工程',
        'business': '工商管理',
        'medicine': '临床医学'
    }
    
    unique_majors = list(major_map.values())
    class_major_return_rate_data = {
        'class_labels': ['大一', '大二', '大三', '大四'],
        'major_labels': unique_majors,
        'data': [[0 for _ in range(4)] for _ in range(len(unique_majors))]
    }
    
    for item in class_major_stats:
        major_name = major_map.get(item['major'], item['major'])
        if major_name in unique_majors:
            major_idx = unique_majors.index(major_name)
            if item['class_status'] in class_map:
                class_idx = class_map[item['class_status']]
                rate = round((item['returned'] / item['total']) * 100, 2) if item['total'] > 0 else 0
                class_major_return_rate_data['data'][major_idx][class_idx] = rate
    
    # 新增：返校方式与年级交叉分析数据
    method_class_stats = returned_queryset.values('class_status', 'return_method').annotate(count=Count('id'))
    
    method_map = {'train': '火车', 'plane': '飞机', 'bus': '汽车', 'private_car': '私家车', 'other': '其他'}
    
    method_class_data = {
        'class_labels': ['大一', '大二', '大三', '大四'],
        'method_labels': ['火车', '飞机', '汽车', '私家车', '其他'],
        'data': [[0 for _ in range(4)] for _ in range(5)]
    }
    
    for item in method_class_stats:
        method_name = method_map.get(item['return_method'], item['return_method'])
        if method_name in method_class_data['method_labels']:
            method_idx = method_class_data['method_labels'].index(method_name)
            if item['class_status'] in class_map:
                class_idx = class_map[item['class_status']]
                method_class_data['data'][method_idx][class_idx] = item['count']
    
    data = {
        'total_students': total_students,
        'return_status_data': return_status_data,
        'class_status_data': class_status_data,
        'major_data': major_data,
        'return_method_data': return_method_data,
        'daily_return_data': daily_return_data,
        'gender_data': gender_data,
        'return_rate': return_rate,
        'not_return_rate': not_return_rate,
        'delayed_rate': delayed_rate,
        'major_return_rate_data': major_return_rate_data,
        'class_return_rate_data': class_return_rate_data,
        'gender_return_status_data': gender_return_status_data,
        'return_time_distribution_data': return_time_distribution_data,
        'class_major_return_rate_data': class_major_return_rate_data,
        'method_class_data': method_class_data,
    }
    
    return JsonResponse(data)


def user_login(request):
    """用户登录视图"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'dashboard/login.html')


def user_register(request):
    """用户注册视图"""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        # 验证密码是否匹配
        if password1 != password2:
            messages.error(request, '两次输入的密码不一致')
            return redirect('register')
        
        # 验证用户名是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
            return redirect('register')
        
        # 验证邮箱是否已存在
        if User.objects.filter(email=email).exists():
            messages.error(request, '邮箱已被注册')
            return redirect('register')
        
        # 创建新用户
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        messages.success(request, '注册成功，请登录')
        return redirect('login')
    
    return render(request, 'dashboard/register.html')


def user_logout(request):
    """用户注销视图"""
    logout(request)
    return redirect('login')


@login_required
def export_students_csv(request):
    """导出学生数据为CSV格式"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    
    writer = csv.writer(response)
    # 写入CSV表头
    writer.writerow([
        '学号', '姓名', '性别', '年级', '专业', '返校状态', 
        '返校时间', '返校方式', '联系电话', '备注'
    ])
    
    # 查询所有学生数据
    students = Student.objects.all()
    
    # 定义数据映射
    gender_map = {'male': '男', 'female': '女'}
    class_map = {'freshman': '大一', 'sophomore': '大二', 'junior': '大三', 'senior': '大四'}
    major_map = {
        'computer': '计算机科学与技术',
        'electronics': '电子信息工程',
        'mechanical': '机械工程',
        'civil': '土木工程',
        'business': '工商管理',
        'medicine': '临床医学'
    }
    return_status_map = {'returned': '已返校', 'not_returned': '未返校', 'delayed': '延期返校'}
    return_method_map = {'train': '火车', 'plane': '飞机', 'bus': '汽车', 'private_car': '私家车', 'other': '其他'}
    
    # 写入数据行
    for student in students:
        writer.writerow([
            student.student_id,
            student.name,
            gender_map.get(student.gender, student.gender),
            class_map.get(student.class_status, student.class_status),
            major_map.get(student.major, student.major),
            return_status_map.get(student.return_status, student.return_status),
            student.return_time.strftime('%Y-%m-%d %H:%M:%S') if student.return_time else '',
            return_method_map.get(student.return_method, student.return_method),
            student.contact,
            student.remarks
        ])
    
    return response


@login_required
def export_students_excel(request):
    """导出学生数据为Excel格式"""
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="students.xls"'
    
    # 创建Excel工作簿
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('学生返校数据')
    
    # 定义样式
    style_header = xlwt.easyxf(
        'font: bold on, height 200; align: horiz center; borders: top thin, bottom thin, left thin, right thin'
    )
    style_data = xlwt.easyxf('borders: top thin, bottom thin, left thin, right thin')
    
    # 定义数据映射
    gender_map = {'male': '男', 'female': '女'}
    class_map = {'freshman': '大一', 'sophomore': '大二', 'junior': '大三', 'senior': '大四'}
    major_map = {
        'computer': '计算机科学与技术',
        'electronics': '电子信息工程',
        'mechanical': '机械工程',
        'civil': '土木工程',
        'business': '工商管理',
        'medicine': '临床医学'
    }
    return_status_map = {'returned': '已返校', 'not_returned': '未返校', 'delayed': '延期返校'}
    return_method_map = {'train': '火车', 'plane': '飞机', 'bus': '汽车', 'private_car': '私家车', 'other': '其他'}
    
    # 写入表头
    headers = ['学号', '姓名', '性别', '年级', '专业', '返校状态', '返校时间', '返校方式', '联系电话', '备注']
    for col_idx, header in enumerate(headers):
        ws.write(0, col_idx, header, style_header)
    
    # 查询所有学生数据
    students = Student.objects.all()
    
    # 设置列宽
    col_widths = [256 * 12, 256 * 10, 256 * 6, 256 * 8, 256 * 18, 256 * 12, 256 * 18, 256 * 12, 256 * 15, 256 * 30]
    for col_idx, width in enumerate(col_widths):
        ws.col(col_idx).width = width
    
    # 写入数据行
    for row_idx, student in enumerate(students, start=1):
        ws.write(row_idx, 0, student.student_id, style_data)
        ws.write(row_idx, 1, student.name, style_data)
        ws.write(row_idx, 2, gender_map.get(student.gender, student.gender), style_data)
        ws.write(row_idx, 3, class_map.get(student.class_status, student.class_status), style_data)
        ws.write(row_idx, 4, major_map.get(student.major, student.major), style_data)
        ws.write(row_idx, 5, return_status_map.get(student.return_status, student.return_status), style_data)
        
        if student.return_time:
            ws.write(row_idx, 6, student.return_time.strftime('%Y-%m-%d %H:%M:%S'), style_data)
        else:
            ws.write(row_idx, 6, '', style_data)
            
        ws.write(row_idx, 7, return_method_map.get(student.return_method, student.return_method), style_data)
        ws.write(row_idx, 8, student.contact, style_data)
        ws.write(row_idx, 9, student.remarks, style_data)
    
    # 保存Excel文件到响应
    wb.save(response)
    
    return response


@login_required
def student_list(request):
    """学生列表页面"""
    # 获取筛选参数
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    class_status = request.GET.get('class_status')
    major = request.GET.get('major')
    return_status = request.GET.get('return_status')
    
    # 构建查询集
    queryset = Student.objects.all()
    
    # 应用筛选条件
    if start_date and end_date:
        queryset = queryset.filter(return_time__date__range=[start_date, end_date])
    elif start_date:
        queryset = queryset.filter(return_time__date__gte=start_date)
    elif end_date:
        queryset = queryset.filter(return_time__date__lte=end_date)
    
    if class_status:
        queryset = queryset.filter(class_status=class_status)
    
    if major:
        queryset = queryset.filter(major=major)
    
    if return_status:
        queryset = queryset.filter(return_status=return_status)
    
    # 处理批量操作
    if request.method == 'POST':
        action = request.POST.get('action')
        selected_students = request.POST.getlist('selected_students')
        
        if not selected_students:
            messages.error(request, '请先选择要操作的学生！')
        else:
            students = Student.objects.filter(id__in=selected_students)
            
            if action == 'batch_delete':
                # 批量删除
                students.delete()
                messages.success(request, f'成功删除 {len(selected_students)} 名学生！')
            elif action == 'batch_update_status':
                # 批量更新返校状态
                new_return_status = request.POST.get('new_return_status')
                if new_return_status:
                    # 使用bulk_update进行批量更新
                    students.update(return_status=new_return_status)
                    messages.success(request, f'成功更新 {len(selected_students)} 名学生的返校状态！')
                else:
                    messages.error(request, '请选择要更新的返校状态！')
    
    # 分页
    from django.core.paginator import Paginator
    paginator = Paginator(queryset, 20)  # 每页20条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/student_list.html', {'page_obj': page_obj})


@login_required
def student_detail(request, student_id):
    """学生详情页面"""
    student = Student.objects.get(id=student_id)
    return render(request, 'dashboard/student_detail.html', {'student': student})


@login_required
def student_create(request):
    """创建新学生"""
    if request.method == 'POST':
        # 处理表单提交
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        class_status = request.POST.get('class_status')
        major = request.POST.get('major')
        return_status = request.POST.get('return_status')
        contact = request.POST.get('contact')
        remarks = request.POST.get('remarks')
        
        return_time_str = request.POST.get('return_time')
        if return_time_str:
            from datetime import datetime
            return_time = datetime.strptime(return_time_str, '%Y-%m-%d %H:%M:%S')
        else:
            return_time = None
        
        return_method = request.POST.get('return_method')
        
        # 创建新学生
        student = Student.objects.create(
            student_id=student_id,
            name=name,
            gender=gender,
            class_status=class_status,
            major=major,
            return_status=return_status,
            return_time=return_time,
            return_method=return_method,
            contact=contact,
            remarks=remarks
        )
        
        # 重定向到学生详情页面
        return redirect('student_detail', student_id=student.id)
    
    return render(request, 'dashboard/student_create.html')


@login_required
def student_edit(request, student_id):
    """编辑学生信息"""
    student = Student.objects.get(id=student_id)
    
    if request.method == 'POST':
        # 处理表单提交
        student.name = request.POST.get('name')
        student.gender = request.POST.get('gender')
        student.class_status = request.POST.get('class_status')
        student.major = request.POST.get('major')
        student.return_status = request.POST.get('return_status')
        
        return_time_str = request.POST.get('return_time')
        if return_time_str:
            from datetime import datetime
            student.return_time = datetime.strptime(return_time_str, '%Y-%m-%dT%H:%M')
        else:
            student.return_time = None
        
        student.return_method = request.POST.get('return_method')
        student.contact = request.POST.get('contact')
        student.remarks = request.POST.get('remarks')
        student.save()
        
        # 重定向到学生详情页面
        return redirect('student_detail', student_id=student.id)
    
    return render(request, 'dashboard/student_edit.html', {'student': student})


@login_required
def student_delete(request, student_id):
    """删除学生信息"""
    student = Student.objects.get(id=student_id)
    
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    
    return render(request, 'dashboard/student_delete_confirm.html', {'student': student})


@login_required
def import_students(request):
    """导入学生数据"""
    if request.method == 'POST':
        file = request.FILES.get('file')
        import_type = request.POST.get('import_type')
        
        if not file:
            messages.error(request, '请选择要导入的文件！')
            return redirect('import_students')
        
        if not import_type:
            messages.error(request, '请选择导入文件类型！')
            return redirect('import_students')
        
        # 保存上传的文件
        file_path = os.path.join(settings.MEDIA_ROOT, 'imports', file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        try:
            if import_type == 'csv':
                # 处理CSV文件
                success_count = process_csv_import(file_path)
            elif import_type == 'excel':
                # 处理Excel文件
                success_count = process_excel_import(file_path)
            else:
                messages.error(request, '不支持的文件类型！')
                return redirect('import_students')
            
            messages.success(request, f'成功导入 {success_count} 条学生数据！')
        except Exception as e:
            messages.error(request, f'导入失败：{str(e)}')
        finally:
            # 清理临时文件
            if os.path.exists(file_path):
                os.remove(file_path)
        
        return redirect('student_list')
    
    return render(request, 'dashboard/import_students.html')


def process_csv_import(file_path):
    """处理CSV文件导入"""
    success_count = 0
    
    # 定义映射关系
    gender_map = {'男': 'male', '女': 'female'}
    class_map = {'大一': 'freshman', '大二': 'sophomore', '大三': 'junior', '大四': 'senior'}
    major_map = {
        '计算机科学与技术': 'computer',
        '电子信息工程': 'electronics',
        '机械工程': 'mechanical',
        '土木工程': 'civil',
        '工商管理': 'business',
        '临床医学': 'medicine'
    }
    return_status_map = {'已返校': 'returned', '未返校': 'not_returned', '延期返校': 'delayed'}
    return_method_map = {'火车': 'train', '飞机': 'plane', '汽车': 'bus', '私家车': 'private_car', '其他': 'other'}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 转换数据格式
            gender = gender_map.get(row.get('性别'), 'male')
            class_status = class_map.get(row.get('年级'), 'freshman')
            major = major_map.get(row.get('专业'), 'computer')
            return_status = return_status_map.get(row.get('返校状态'), 'not_returned')
            return_method = return_method_map.get(row.get('返校方式'), '')
            
            # 处理返校时间
            return_time_str = row.get('返校时间')
            return_time = None
            if return_time_str:
                from datetime import datetime
                try:
                    return_time = datetime.strptime(return_time_str, '%Y-%m-%d %H:%M:%S')
                except:
                    try:
                        return_time = datetime.strptime(return_time_str, '%Y-%m-%d')
                    except:
                        return_time = None
            
            # 创建或更新学生记录
            Student.objects.update_or_create(
                student_id=row.get('学号'),
                defaults={
                    'name': row.get('姓名'),
                    'gender': gender,
                    'class_status': class_status,
                    'major': major,
                    'return_status': return_status,
                    'return_time': return_time,
                    'return_method': return_method,
                    'contact': row.get('联系电话'),
                    'remarks': row.get('备注')
                }
            )
            
            success_count += 1
    
    return success_count


def process_excel_import(file_path):
    """处理Excel文件导入"""
    success_count = 0
    
    # 打开Excel文件
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_index(0)  # 使用第一个工作表
    
    # 定义映射关系
    gender_map = {'男': 'male', '女': 'female'}
    class_map = {'大一': 'freshman', '大二': 'sophomore', '大三': 'junior', '大四': 'senior'}
    major_map = {
        '计算机科学与技术': 'computer',
        '电子信息工程': 'electronics',
        '机械工程': 'mechanical',
        '土木工程': 'civil',
        '工商管理': 'business',
        '临床医学': 'medicine'
    }
    return_status_map = {'已返校': 'returned', '未返校': 'not_returned', '延期返校': 'delayed'}
    return_method_map = {'火车': 'train', '飞机': 'plane', '汽车': 'bus', '私家车': 'private_car', '其他': 'other'}
    
    # 获取表头
    header = [cell.value for cell in sheet.row(0)]
    
    # 处理数据行
    for row_idx in range(1, sheet.nrows):
        row = sheet.row(row_idx)
        row_data = {header[i]: cell.value for i, cell in enumerate(row)}
        
        # 转换数据格式
        gender = gender_map.get(row_data.get('性别'), 'male')
        class_status = class_map.get(row_data.get('年级'), 'freshman')
        major = major_map.get(row_data.get('专业'), 'computer')
        return_status = return_status_map.get(row_data.get('返校状态'), 'not_returned')
        return_method = return_method_map.get(row_data.get('返校方式'), '')
        
        # 处理返校时间
        return_time = None
        return_time_cell = row_data.get('返校时间')
        if return_time_cell and isinstance(return_time_cell, (int, float)):
            try:
                from datetime import datetime
                return_time = xlrd.xldate.xldate_as_datetime(return_time_cell, workbook.datemode)
            except:
                pass
        elif isinstance(return_time_cell, str):
            try:
                return_time = datetime.strptime(return_time_cell, '%Y-%m-%d %H:%M:%S')
            except:
                try:
                    return_time = datetime.strptime(return_time_cell, '%Y-%m-%d')
                except:
                    pass
        
        # 创建或更新学生记录
        Student.objects.update_or_create(
            student_id=row_data.get('学号'),
            defaults={
                'name': row_data.get('姓名'),
                'gender': gender,
                'class_status': class_status,
                'major': major,
                'return_status': return_status,
                'return_time': return_time,
                'return_method': return_method,
                'contact': row_data.get('联系电话'),
                'remarks': row_data.get('备注')
            }
        )
        
        success_count += 1
    
    return success_count
