from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class PersonalInfo(models.Model):
    """
    个人信息模型
    
    存储个人的基本信息、联系方式和社交媒体链接等。
    该模型设计为单例使用，通常只需要一条记录。
    
    字段说明：
        name: 姓名
        title: 职位或头衔
        short_bio: 简短简介，用于首页展示
        bio: 详细个人简介，用于关于我页面
        avatar: 头像图片
        email: 邮箱地址
        phone: 电话号码
        website: 个人网站链接
        github: GitHub账号链接
        linkedin: LinkedIn账号链接
        twitter: Twitter/X账号链接
        instagram: Instagram账号链接
        meta: Meta/Facebook账号链接
        created_at: 创建时间
        updated_at: 更新时间
    """
    name = models.CharField(max_length=100, verbose_name=_('姓名'))
    title = models.CharField(max_length=200, verbose_name=_('职位'))
    short_bio = models.TextField(verbose_name=_('简短简介'), blank=True, null=True)
    bio = models.TextField(verbose_name=_('个人简介'))
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_('头像'))
    email = models.EmailField(max_length=254, verbose_name=_('邮箱'))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('电话'))
    website = models.URLField(max_length=200, blank=True, null=True, verbose_name=_('个人网站'))
    github = models.URLField(max_length=200, blank=True, null=True, verbose_name=_('GitHub'))
    linkedin = models.URLField(max_length=200, blank=True, null=True, verbose_name=_('LinkedIn'))
    twitter = models.URLField(max_length=200, blank=True, null=True, verbose_name=_('Twitter'))
    instagram = models.URLField(max_length=200, blank=True, null=True, verbose_name=_('Instagram'))
    meta = models.URLField(max_length=200, blank=True, null=True, verbose_name=_('Meta/Facebook'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('创建时间'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('更新时间'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('个人信息')
        verbose_name_plural = _('个人信息')


class Project(models.Model):
    """
    作品集模型
    
    存储个人项目的详细信息，包括项目名称、描述、类别、图片等。
    用于在作品集页面展示和管理个人项目。
    
    字段说明：
        title: 项目名称
        slug: URL别名，用于生成友好的项目详情页URL
        description: 项目详细描述
        category: 项目类别，如游戏开发、前端设计等
        image: 项目图片
        link: 项目访问链接
        github_link: 项目GitHub仓库链接
        start_date: 项目开始日期
        end_date: 项目结束日期，可为空（表示进行中）
        is_active: 是否在网站上展示
        created_at: 创建时间
        updated_at: 更新时间
    """
    title = models.CharField(max_length=200, verbose_name=_('项目名称'))
    slug = models.SlugField(unique=True, verbose_name=_('URL 别名'), help_text=_('项目在 URL 中的唯一标识'), null=True, blank=True)
    description = models.TextField(verbose_name=_('项目描述'))
    category = models.CharField(max_length=100, verbose_name=_('项目类别'))
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name=_('项目图片'))
    link = models.URLField(max_length=200, blank=True, null=True, verbose_name=_('项目链接'))
    github_link = models.URLField(max_length=200, blank=True, null=True, verbose_name=_('GitHub链接'))
    start_date = models.DateField(verbose_name=_('开始日期'))
    end_date = models.DateField(blank=True, null=True, verbose_name=_('结束日期'))
    is_active = models.BooleanField(default=True, verbose_name=_('是否展示'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('创建时间'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('更新时间'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('作品集')
        verbose_name_plural = _('作品集')
        ordering = ['-created_at']


class Video(models.Model):
    """
    视频模型
    
    存储项目相关的视频文件，支持主视频和多个辅助视频。
    每个项目可以有多个视频，但最多只能有一个主视频。
    
    字段说明：
        project: 所属项目，外键关联到Project模型
        title: 视频标题
        description: 视频描述
        video_file: 视频文件
        thumbnail: 视频缩略图
        duration: 视频时长（秒）
        is_main: 是否为主视频
        order: 视频排序顺序
        is_visible: 是否在网站上可见
        created_at: 创建时间
        updated_at: 更新时间
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='videos', verbose_name=_('所属项目'))
    title = models.CharField(max_length=200, verbose_name=_('视频标题'))
    description = models.TextField(blank=True, null=True, verbose_name=_('视频描述'))
    video_file = models.FileField(upload_to='videos/', verbose_name=_('视频文件'))
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True, verbose_name=_('视频缩略图'))
    duration = models.IntegerField(blank=True, null=True, verbose_name=_('视频时长（秒）'), help_text=_('自动计算或手动输入'))
    # category = models.CharField(max_length=100, default='其他', verbose_name=_('视频分类'))
    is_main = models.BooleanField(default=False, verbose_name=_('是否为主视频'), help_text=_('每个项目最多一个主视频'))
    order = models.IntegerField(default=0, verbose_name=_('排序顺序'))
    is_visible = models.BooleanField(default=True, verbose_name=_('是否可见'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('创建时间'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('更新时间'))

    def __str__(self):
        return f"{self.project.title} - {self.title}"

    class Meta:
        verbose_name = _('视频')
        verbose_name_plural = _('视频')
        ordering = ['-is_main', 'order', '-created_at']
        # unique_together = [['project', 'is_main']]  # 保证每个项目最多一个主视频


class Certificate(models.Model):
    """
    证书模型
    
    存储个人获得的证书和资质，用于在关于我页面展示个人技能和成就。
    
    字段说明：
        name: 证书名称
        issuing_authority: 颁发机构
        issue_date: 颁发日期
        certificate_id: 证书编号
        description: 证书描述
        image: 证书图片
        is_visible: 是否在网站上可见
        created_at: 创建时间
        updated_at: 更新时间
    """
    name = models.CharField(max_length=200, verbose_name=_('证书名称'))
    issuing_authority = models.CharField(max_length=200, verbose_name=_('颁发机构'))
    issue_date = models.DateField(verbose_name=_('颁发日期'))
    certificate_id = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('证书编号'))
    description = models.TextField(blank=True, null=True, verbose_name=_('证书描述'))
    image = models.ImageField(upload_to='certificates/', blank=True, null=True, verbose_name=_('证书图片'))
    is_visible = models.BooleanField(default=True, verbose_name=_('是否可见'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('创建时间'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('更新时间'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('证书')
        verbose_name_plural = _('证书')
        ordering = ['-issue_date']
