# Generated migration for adding Video model

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_project_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='视频标题')),
                ('description', models.TextField(blank=True, null=True, verbose_name='视频描述')),
                ('video_file', models.FileField(upload_to='videos/', verbose_name='视频文件')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='video_thumbnails/', verbose_name='视频缩略图')),
                ('duration', models.IntegerField(blank=True, help_text='自动计算或手动输入', null=True, verbose_name='视频时长（秒）')),
                ('is_main', models.BooleanField(default=False, help_text='每个项目最多一个主视频', verbose_name='是否为主视频')),
                ('order', models.IntegerField(default=0, verbose_name='排序顺序')),
                ('is_visible', models.BooleanField(default=True, verbose_name='是否可见')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='portfolio.project', verbose_name='所属项目')),
            ],
            options={
                'verbose_name': '视频',
                'verbose_name_plural': '视频',
                'ordering': ['-is_main', 'order', '-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='video',
            constraint=models.UniqueConstraint(fields=['project', 'is_main'], name='unique_main_video_per_project', condition=models.Q(('is_main', True))),
        ),
    ]
