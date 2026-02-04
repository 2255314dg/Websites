import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'profile_website.settings')
import django
try:
    django.setup()
    from django.template.loader import render_to_string
    from portfolio.models import Project, Video
    p = Project.objects.get(slug='video')
    videos = Video.objects.filter(project=p, is_visible=True)
    main_video = videos.filter(is_main=True).first()
    other_videos = videos.filter(is_main=False).order_by('order')
    context = {'project': p, 'main_video': main_video, 'other_videos': other_videos}
    html = render_to_string('project_detail.html', context)
    print('Rendered length:', len(html))
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
