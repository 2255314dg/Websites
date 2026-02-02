#!/usr/bin/env python
"""
视频缩略图生成脚本
根据视频文件自动生成缩略图，或使用默认占位图
"""

import os
import sys
import django
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import colorsys
import random

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'profile_website.settings')
django.setup()

from portfolio.models import Video
from django.core.files.base import ContentFile
import io

# 媒体路径配置
MEDIA_ROOT = Path('media')
VIDEOS_DIR = MEDIA_ROOT / 'videos'
VIDEO_THUMBNAILS_DIR = MEDIA_ROOT / 'video_thumbnails'

# 确保缩略图目录存在
VIDEO_THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)

def generate_default_thumbnail(title, video_id, color=None):
    """
    生成默认的视频缩略图（带标题文字）
    
    Args:
        title: 视频标题
        video_id: 视频ID
        color: 背景颜色 (R, G, B)，如果为None则随机生成
    
    Returns:
        PIL Image对象
    """
    # 如果没有指定颜色，生成随机渐变色
    if color is None:
        hue = random.random()
        saturation = 0.7
        value = 0.9
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        color = (int(r * 255), int(g * 255), int(b * 255))
    
    # 创建图像 (16:9 比例)
    width, height = 640, 360
    image = Image.new('RGB', (width, height), color)
    
    # 添加渐变效果
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            factor = x / width
            new_color = tuple(int(c * (0.7 + 0.3 * factor)) for c in color)
            pixels[x, y] = new_color
    
    # 添加播放按钮图标背景
    draw = ImageDraw.Draw(image)
    
    # 在中心画一个圆形播放按钮
    button_size = 80
    button_x = (width - button_size) // 2
    button_y = (height - button_size) // 2
    
    # 外圆 (白色)
    draw.ellipse(
        [button_x, button_y, button_x + button_size, button_y + button_size],
        fill='white',
        outline='white'
    )
    
    # 内三角形 (播放符号)
    triangle_points = [
        (button_x + button_size * 0.35, button_y + button_size * 0.25),
        (button_x + button_size * 0.35, button_y + button_size * 0.75),
        (button_x + button_size * 0.75, button_y + button_size * 0.5)
    ]
    draw.polygon(triangle_points, fill=color)
    
    # 添加标题文字（如果标题不太长）
    if len(title) <= 20:
        try:
            # 尝试使用系统字体（可能不存在，使用默认字体）
            font_size = 20
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # 在底部添加标题
        text_y = height - 50
        text_bbox = draw.textbbox((0, 0), title, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (width - text_width) // 2
        
        # 添加半透明背景
        draw.rectangle(
            [text_x - 10, text_y - 5, text_x + text_width + 10, text_y + 25],
            fill=(0, 0, 0, 128)
        )
        draw.text((text_x, text_y), title, fill='white', font=font)
    
    return image

def create_video_thumbnails():
    """为所有没有缩略图的视频创建默认缩略图"""
    
    videos = Video.objects.filter(is_visible=True)
    created_count = 0
    updated_count = 0
    
    print("开始生成视频缩略图...")
    print(f"找到 {videos.count()} 个视频")
    
    for video in videos:
        # 如果已有缩略图，跳过
        if video.thumbnail:
            print(f"✓ {video.title} - 已有缩略图，跳过")
            continue
        
        # 生成新缩略图
        try:
            print(f"正在生成缩略图: {video.title}...", end=' ')
            
            # 生成缩略图
            thumbnail = generate_default_thumbnail(video.title, video.id)
            
            # 保存为文件
            thumbnail_filename = f"{video.id}_thumb.jpg"
            thumbnail_path = VIDEO_THUMBNAILS_DIR / thumbnail_filename
            
            # 保存图像
            thumbnail.save(thumbnail_path, 'JPEG', quality=85)
            
            # 更新数据库中的缩略图路径
            relative_path = f"video_thumbnails/{thumbnail_filename}"
            video.thumbnail = relative_path
            video.save(update_fields=['thumbnail'])
            
            created_count += 1
            print(f"✓ 成功")
        except Exception as e:
            print(f"✗ 失败: {str(e)}")
    
    print(f"\n生成完成！")
    print(f"新创建缩略图: {created_count}")
    print(f"已有缩略图: {updated_count}")

def list_videos():
    """列出所有视频及其详细信息"""
    videos = Video.objects.select_related('project').all()
    
    if not videos.exists():
        print("没有找到任何视频")
        return
    
    print("\n=== 视频列表 ===\n")
    for video in videos:
        status = "✓ 可见" if video.is_visible else "✗ 隐藏"
        main_status = "【主视频】" if video.is_main else ""
        print(f"ID: {video.id}")
        print(f"  标题: {video.title} {main_status}")
        print(f"  项目: {video.project.title}")
        print(f"  描述: {video.description[:50]}...")
        print(f"  视频文件: {video.video_file.name if video.video_file else '未设置'}")
        print(f"  缩略图: {video.thumbnail.name if video.thumbnail else '无'}")
        print(f"  时长: {video.duration}秒" if video.duration else "  时长: 未设置")
        print(f"  排序: {video.order}")
        print(f"  状态: {status}")
        print()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'generate':
            create_video_thumbnails()
        elif command == 'list':
            list_videos()
        else:
            print(f"未知命令: {command}")
            print("用法: python manage.py shell < video_manager.py")
    else:
        print("视频管理工具")
        print("用法:")
        print("  python video_manager.py generate  - 生成视频缩略图")
        print("  python video_manager.py list      - 列出所有视频")
