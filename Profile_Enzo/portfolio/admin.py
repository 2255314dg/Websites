from django.contrib import admin
from .models import PersonalInfo, Project, Certificate, Video

# Register your models here.

@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'updated_at']
    fields = ['name', 'title', 'bio', 'short_bio', 'email', 'phone',
              'website', 'github', 'linkedin', 'instagram', 'avatar', 'meta']
    
    def has_add_permission(self, request):
        # 只允许一个PersonalInfo记录
        return not PersonalInfo.objects.exists()

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuing_authority', 'issue_date', 'is_visible']
    list_filter = ['is_visible', 'issue_date']
    search_fields = ['name', 'issuing_authority']
    fieldsets = (
        ('基本信息', {
            'fields': ['name', 'issuing_authority', 'issue_date', 'certificate_id']
        }),
        ('描述和媒体', {
            'fields': ['description', 'image']
        }),
        ('显示设置', {
            'fields': ['is_visible']
        })
    )

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'start_date', 'is_active']
    list_filter = ['category', 'is_active', 'start_date']
    search_fields = ['title', 'description']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ['title', 'slug', 'category', 'description']
        }),
        ('日期和状态', {
            'fields': ['start_date', 'end_date', 'is_active']
        }),
        ('链接和媒体', {
            'fields': ['image', 'link', 'github_link']
        }),
        ('元数据', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    )

class VideoInline(admin.TabularInline):
    """视频内联编辑器 - 在Project编辑页面显示关联视频"""
    model = Video
    extra = 1
    fields = ['title', 'is_main', 'is_visible', 'order', 'duration']
    readonly_fields = ['created_at']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'is_main', 'is_visible', 'order', 'duration', 'created_at']
    list_filter = ['is_main', 'is_visible', 'project', 'created_at']
    search_fields = ['title', 'description', 'project__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ['project', 'title', 'description']
        }),
        ('视频文件和缩略图', {
            'fields': ['video_file', 'thumbnail']
        }),
        ('视频详情', {
            'fields': ['duration', 'order']
        }),
        ('显示设置', {
            'fields': ['is_main', 'is_visible']
        }),
        ('元数据', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    )
    
    def save_model(self, request, obj, form, change):
        """保存前的验证"""
        # 如果设置为主视频，检查项目是否已有其他主视频
        if obj.is_main:
            # 获取该项目的其他主视频
            other_main_videos = Video.objects.filter(
                project=obj.project,
                is_main=True
            ).exclude(id=obj.id)
            
            # 如果有其他主视频，取消它们的主视频标记
            if other_main_videos.exists():
                other_main_videos.update(is_main=False)
        
        super().save_model(request, obj, form, change)

# 将VideoInline添加到ProjectAdmin
ProjectAdmin.inlines = [VideoInline]

