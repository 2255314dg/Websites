from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class PersonalInfo(models.Model):
    """个人信息模型"""
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
    """作品集模型"""
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
    """视频模型 - 关联到项目"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='videos', verbose_name=_('所属项目'))
    title = models.CharField(max_length=200, verbose_name=_('视频标题'))
    description = models.TextField(blank=True, null=True, verbose_name=_('视频描述'))
    video_file = models.FileField(upload_to='videos/', verbose_name=_('视频文件'))
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True, verbose_name=_('视频缩略图'))
    duration = models.IntegerField(blank=True, null=True, verbose_name=_('视频时长（秒）'), help_text=_('自动计算或手动输入'))
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
        unique_together = [['project', 'is_main']]  # 保证每个项目最多一个主视频


class Certificate(models.Model):
    """证书模型"""
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
