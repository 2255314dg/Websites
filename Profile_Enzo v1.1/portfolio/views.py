
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import PersonalInfo, Project, Certificate, Video

# 项目图片映射字典 - 用于根据项目类型映射对应的图片路径
PROJECT_IMAGE_MAPPING = {
    '移动端游戏开发': 'pictures/移动端游戏开发.png',
    'PC端联机游戏开发': 'pictures/PC端联机游戏开发.png',
    'PC端单机游戏开发': 'pictures/PC端单机游戏开发.png',
    'AR应用开发': 'pictures/AR开发.png',
    'VR应用开发': 'pictures/VR开发.png',
    '视频剪辑与制作': 'pictures/视频剪辑与制作.png',
    '音频制作与混音': 'pictures/音频制作与混音.png',
    '特效设计与制作': 'pictures/特效设计与制作.png',
    '场景设计': 'pictures/场景设计.jpg',
}

# 分类映射字典 - 用于将具体项目类型映射到大类
CATEGORY_MAPPING = {
    '移动端游戏开发': '游戏开发',
    'PC端联机游戏开发': '游戏开发',
    'PC端单机游戏开发': '游戏开发',
    'AR应用开发': 'AR/VR/MR开发',
    'VR应用开发': 'AR/VR/MR开发',
    '视频剪辑与制作': '后期处理',
    '音频制作与混音': '后期处理',
    '特效设计与制作': '后期处理',
    '场景设计': '后期处理',
}

# 项目类型显示顺序列表 - 用于控制项目在页面中的显示顺序
PROJECT_ORDER = [
    '移动端游戏开发',
    'PC端联机游戏开发',
    'PC端单机游戏开发',
    'AR应用开发',
    'VR应用开发',
    '视频剪辑与制作',
    '音频制作与混音',
    '特效设计与制作',
    '场景设计',
]

# 固定分类列表 - 作品集页面展示的分类顺序 - 用于控制作品集页面中分类筛选按钮的显示顺序
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
    """
    获取项目的备用图片路径
    
    Args:
        project: Project对象，包含项目的标题和分类信息
        
    Returns:
        str: 备用图片的路径，如果没有找到则返回None
    """
    if project.title in PROJECT_IMAGE_MAPPING:
        return PROJECT_IMAGE_MAPPING[project.title]
    if project.category in PROJECT_IMAGE_MAPPING:
        return PROJECT_IMAGE_MAPPING[project.category]
    return None

def get_standard_category(category):
    """
    将项目的分类标准化，映射到更广泛的分类
    
    Args:
        category: str，项目的具体分类
        
    Returns:
        str: 标准化后的分类，如果没有找到映射则返回原分类
    """
    return CATEGORY_MAPPING.get(category, category)

def get_project_order(project):
    """
    获取项目的排序值，用于在作品集页面中排序项目
    
    Args:
        project: Project对象，包含项目的标题信息
        
    Returns:
        int: 项目的排序值，按照PROJECT_ORDER列表中的顺序
    """
    try:
        return PROJECT_ORDER.index(project.title)
    except ValueError:
        return len(PROJECT_ORDER)

def get_standard_category(category):
    """
    将项目的分类标准化，映射到更广泛的分类
    
    Args:
        category: str，项目的具体分类
        
    Returns:
        str: 标准化后的分类，如果没有找到映射则返回原分类
    """
    mapping = {
        '移动端游戏开发': '游戏开发',
        'PC端联机游戏开发': '游戏开发',
        'PC端单机游戏开发': '游戏开发',
        'AR应用开发': 'AR/VR/MR开发',
        'VR应用开发': 'AR/VR/MR开发',
        '视频剪辑与制作': '后期处理',
        '音频制作与混音': '后期处理',
        '特效设计与制作': '后期处理',
        '场景设计': '后期处理',  
    }
    return mapping.get(category, category)

# --- 视图层 --- 
def home(request):
    """
    首页视图函数
    
    Args:
        request: HttpRequest对象，包含请求的信息
        
    Returns:
        HttpResponse对象，渲染首页模板并返回给客户端
        
    功能：
        - 获取个人信息
        - 获取最近3个活跃的项目
        - 将数据传递给模板进行渲染
    """
    personal_info = PersonalInfo.objects.first()
    projects = Project.objects.filter(is_active=True)[:3]
    context = {
        'personal_info': personal_info,
        'projects': projects,
    }
    return render(request, 'portfolio/home.html', context)

def about(request):
    """
    关于我页面视图函数
    
    Args:
        request: HttpRequest对象，包含请求的信息
        
    Returns:
        HttpResponse对象，渲染关于我页面模板并返回给客户端
        
    功能：
        - 获取个人信息
        - 获取所有可见的证书
        - 将数据传递给模板进行渲染
    """
    personal_info = PersonalInfo.objects.first()
    certificates = Certificate.objects.filter(is_visible=True)
    context = {
        'personal_info': personal_info,
        'certificates': certificates,
    }
    return render(request, 'portfolio/about.html', context)


def portfolio(request):
    """
    作品集页面视图函数
    
    Args:
        request: HttpRequest对象，包含请求的信息
        
    Returns:
        HttpResponse对象，渲染作品集页面模板并返回给客户端
        
    功能：
        - 获取所有活跃的项目
        - 为每个项目添加标准化分类和备用图片
        - 按照预设顺序排序项目
        - 根据请求参数过滤项目分类
        - 实现项目分页
        - 将数据传递给模板进行渲染
    """
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
    return render(request, 'portfolio/portfolio.html', context)

def project_detail(request, project_slug):
    """
    项目详情页面视图函数
    
    Args:
        request: HttpRequest对象，包含请求的信息
        project_slug: str，项目的slug字段，用于唯一标识项目
        
    Returns:
        HttpResponse对象，渲染项目详情页面模板并返回给客户端
        
    功能：
        - 根据slug获取项目详情，如果不存在则返回404错误
        - 为项目添加标准化分类
        - 获取项目相关的所有可见视频
        - 区分主视频和其他视频
        - 添加静态视频卡片
        - 实现视频分页功能
        - 将数据传递给模板进行渲染
    """
    project = get_object_or_404(Project, slug=project_slug)
    project.standard_category = get_standard_category(project.category)
    videos = Video.objects.filter(project=project, is_visible=True)
    main_video = videos.filter(is_main=True).first()
    other_videos = list(videos.filter(is_main=False).order_by('order'))
    
    # 创建静态视频对象
    class StaticVideo:
        def __init__(self, title):
            self.title = title
            self.id = f'static_{title}'
            self.thumbnail = None
            self.duration = None
            self.description = None
            self.video_file = type('obj', (object,), {'url': ''})
    
    # 添加4个静态视频卡片
    static_videos = [StaticVideo(f'{i:03d}') for i in range(1, 5)]
    all_videos = other_videos + static_videos
    
    # 实现视频分页，每页显示6个视频
    per_page = 6
    page_number = request.GET.get('page', 1)
    paginator = Paginator(all_videos, per_page)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'project': project,
        'main_video': main_video,
        'other_videos': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'portfolio/project_detail.html', context)

def contact(request):
    """
    联系方式页面视图函数
    
    Args:
        request: HttpRequest对象，包含请求的信息
        
    Returns:
        HttpResponse对象，渲染联系方式页面模板并返回给客户端
        
    功能：
        - 获取个人信息
        - 将数据传递给模板进行渲染
    """
    personal_info = PersonalInfo.objects.first()
    context = {
        'personal_info': personal_info,
    }
    return render(request, 'portfolio/contact.html', context)


def video(request):
    """
    视频页面视图函数
    
    Args:
        request: HttpRequest对象，包含请求的信息
        
    Returns:
        HttpResponse对象，渲染视频页面模板并返回给客户端
        
    功能：
        - 获取所有可见的视频
        - 支持按分类筛选视频
        - 实现视频分页，每页显示16个视频
        - 将数据传递给模板进行渲染
    """
    # 获取所有可见的视频
    videos_qs = Video.objects.filter(is_visible=True)
    
    # 视频分类列表
    video_categories = ['全部', '旅游系列', '游学系列']
    
    # 获取选中的分类
    selected_category = request.GET.get('category', '全部')
    
    # 根据分类筛选视频
    if selected_category != '全部':
        # 由于梦回上海滩视频的分类是"全部"和"旅游系列"，所以当选择"游学系列"时，不显示任何视频
        # 这里我们手动实现分类筛选，因为数据库中还没有category字段
        if selected_category == '游学系列':
            videos_qs = videos_qs.none()  # 游学系列为空
        elif selected_category == '旅游系列':
            # 只显示梦回上海滩视频
            pass  # 暂时保持不变，因为我们在模板中硬编码了视频
    
    # 实现分页，每页显示4个视频
    per_page = 4
    page_number = request.GET.get('page', 1)
    paginator = Paginator(videos_qs, per_page)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'videos': page_obj,
        'video_categories': video_categories,
        'selected_category': selected_category,
        'page_obj': page_obj,
    }
    return render(request, 'portfolio/video.html', context)
