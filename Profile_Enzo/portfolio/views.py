
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import PersonalInfo, Project, Certificate, Video



# --- 工具层 ---
PROJECT_IMAGE_MAPPING = {
    '移动端游戏开发': 'pictures/移动端游戏开发.png',
    'PC端联机游戏开发': 'pictures/PC端联机游戏开发.png',
    'PC端单机游戏开发': 'pictures/PC端单机游戏开发.png',
    'AR应用开发': 'pictures/AR开发.png',
    'VR应用开发': 'pictures/VR开发.png',
    '视频剪辑与制作': 'pictures/视频剪辑与制作.png',
    '音频制作与混音': 'pictures/音频制作与混音.png',
    '特效设计与制作': 'pictures/特效设计与制作.png',
}

CATEGORY_MAPPING = {
    '移动端游戏开发': '游戏开发',
    'PC端联机游戏开发': '游戏开发',
    'PC端单机游戏开发': '游戏开发',
    'AR应用开发': 'AR/VR/MR开发',
    'VR应用开发': 'AR/VR/MR开发',
    '视频剪辑与制作': '后期处理',
    '音频制作与混音': '后期处理',
    '特效设计与制作': '后期处理',
}

PROJECT_ORDER = [
    '移动端游戏开发',
    'PC端联机游戏开发',
    'PC端单机游戏开发',
    'AR应用开发',
    'VR应用开发',
    '视频剪辑与制作',
    '音频制作与混音',
    '特效设计与制作',
]

# 固定分类列表 - 作品集页面展示的分类顺序
PORTFOLIO_CATEGORIES = [
    '前端设计与开发',
    '游戏开发',
    'AR/VR/MR开发',
    '后期处理',
]

# 分类分页配置 - 不同分类可设置不同每页显示数量
CATEGORY_PAGINATION_CONFIG = {
    '游戏开发': 6,              # 游戏开发每页显示6项
    '前端设计与开发': 6,        # 前端设计与开发每页显示6项
    'AR/VR/MR开发': 6,          # AR/VR/MR开发每页显示6项
    '后期处理': 6,              # 后期处理每页显示6项
    'default': 9,               # 其他分类每页显示9项
}

def get_project_fallback_image(project):
    if project.title in PROJECT_IMAGE_MAPPING:
        return PROJECT_IMAGE_MAPPING[project.title]
    if project.category in PROJECT_IMAGE_MAPPING:
        return PROJECT_IMAGE_MAPPING[project.category]
    return None

def get_standard_category(category):
    return CATEGORY_MAPPING.get(category, category)

def get_project_order(project):
    try:
        return PROJECT_ORDER.index(project.title)
    except ValueError:
        return len(PROJECT_ORDER)


# 分类标准化工具
def get_standard_category(category):
    mapping = {
        '移动端游戏开发': '游戏开发',
        'PC端联机游戏开发': '游戏开发',
        'PC端单机游戏开发': '游戏开发',
        'AR应用开发': 'AR/VR/MR开发',
        'VR应用开发': 'AR/VR/MR开发',
        '视频剪辑与制作': '后期处理',
        '音频制作与混音': '后期处理',
        '特效设计与制作': '后期处理',
    }
    return mapping.get(category, category)

# --- 视图层 ---
def home(request):
    """首页视图"""
    personal_info = PersonalInfo.objects.first()
    projects = Project.objects.filter(is_active=True)[:3]
    context = {
        'personal_info': personal_info,
        'projects': projects,
    }
    return render(request, 'home.html', context)

def about(request):
    """关于我页面视图"""
    personal_info = PersonalInfo.objects.first()
    certificates = Certificate.objects.filter(is_visible=True)
    context = {
        'personal_info': personal_info,
        'certificates': certificates,
    }
    return render(request, 'about.html', context)


def portfolio(request):
    """作品集页面视图"""
    projects_qs = Project.objects.filter(is_active=True)
    projects = []
    for project in projects_qs:
        project.standard_category = get_standard_category(project.category)
        project.fallback_image = get_project_fallback_image(project)
        project.image = None
        projects.append(project)

    projects.sort(key=get_project_order)
    categories = PORTFOLIO_CATEGORIES
    selected_category = request.GET.get('category', 'all')
    if selected_category != 'all':
        projects = [p for p in projects if p.standard_category == selected_category]
    per_page = CATEGORY_PAGINATION_CONFIG.get(selected_category, CATEGORY_PAGINATION_CONFIG['default'])
    page_number = request.GET.get('page', 1)
    paginator = Paginator(projects, per_page)
    page_obj = paginator.get_page(page_number)
    context = {
        'projects': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'page_obj': page_obj,
    }
    return render(request, 'portfolio.html', context)

def project_detail(request, project_slug):
    """项目详情页面视图"""
    project = get_object_or_404(Project, slug=project_slug)
    project.standard_category = get_standard_category(project.category)
    videos = Video.objects.filter(project=project, is_visible=True)
    main_video = videos.filter(is_main=True).first()
    other_videos = videos.filter(is_main=False).order_by('order')
    context = {
        'project': project,
        'main_video': main_video,
        'other_videos': other_videos,
    }
    return render(request, 'project_detail.html', context)

def contact(request):
    """联系方式页面视图"""
    personal_info = PersonalInfo.objects.first()
    context = {
        'personal_info': personal_info,
    }
    return render(request, 'contact.html', context)
