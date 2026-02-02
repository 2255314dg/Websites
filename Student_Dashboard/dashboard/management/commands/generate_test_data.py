from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from dashboard.models import Student

class Command(BaseCommand):
    help = '生成学生返校测试数据'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=500, help='生成学生数量')

    def handle(self, *args, **options):
        count = options['count']
        
        # 清除现有数据
        Student.objects.all().delete()
        self.stdout.write(self.style.WARNING('已清除现有数据'))

        # 数据选择
        genders = ['male', 'female']
        class_statuses = ['freshman', 'sophomore', 'junior', 'senior']
        majors = ['computer', 'electronics', 'mechanical', 'civil', 'business', 'medicine']
        return_statuses = ['returned', 'not_returned', 'delayed']
        return_methods = ['train', 'plane', 'bus', 'private_car', 'other']
        
        # 生成随机学生数据
        students = []
        for i in range(count):
            student_id = f'2021{i:05d}' if random.random() > 0.25 else f'2022{i:05d}'
            name = f'学生{i+1}'
            gender = random.choice(genders)
            class_status = random.choice(class_statuses)
            major = random.choice(majors)
            return_status = random.choice(return_statuses)
            
            # 根据返校状态决定返校时间和方式
            if return_status == 'returned':
                # 随机生成最近7天内的返校时间
                days_ago = random.randint(0, 6)
                return_time = timezone.now() - timezone.timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
                return_method = random.choice(return_methods)
            else:
                return_time = None
                return_method = None
            
            contact = f'138{random.randint(10000000, 99999999)}'
            
            student = Student(
                student_id=student_id,
                name=name,
                gender=gender,
                class_status=class_status,
                major=major,
                return_status=return_status,
                return_time=return_time,
                return_method=return_method,
                contact=contact
            )
            students.append(student)
            
            # 每100个学生批量创建一次
            if (i + 1) % 100 == 0:
                Student.objects.bulk_create(students)
                students = []
                self.stdout.write(self.style.SUCCESS(f'已生成 {i+1} 条学生数据'))
        
        # 创建剩余学生数据
        if students:
            Student.objects.bulk_create(students)
            self.stdout.write(self.style.SUCCESS(f'已生成 {count} 条学生数据'))
        
        # 统计生成结果
        total = Student.objects.count()
        returned = Student.objects.filter(return_status='returned').count()
        not_returned = Student.objects.filter(return_status='not_returned').count()
        delayed = Student.objects.filter(return_status='delayed').count()
        
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS(f'测试数据生成完成'))
        self.stdout.write(self.style.SUCCESS(f'总学生数: {total}'))
        self.stdout.write(self.style.SUCCESS(f'已返校: {returned}'))
        self.stdout.write(self.style.SUCCESS(f'未返校: {not_returned}'))
        self.stdout.write(self.style.SUCCESS(f'延期返校: {delayed}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))