from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = '初始化数据库并创建超级用户'

    def handle(self, *args, **options):
        self.stdout.write('开始数据库迁移...')
        call_command('migrate')
        self.stdout.write('数据库迁移完成！')
        
        self.stdout.write('收集静态文件...')
        call_command('collectstatic', '--noinput')
        self.stdout.write('静态文件收集完成！')
        
        self.stdout.write('创建超级用户...')
        # 从环境变量获取超级用户信息
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        # 使用环境变量创建超级用户
        call_command('createsuperuser', '--noinput', 
                    username=username,
                    email=email)
        self.stdout.write('超级用户创建完成！')
        
        # 导入初始数据
        self.stdout.write('导入初始数据...')
        try:
            call_command('loaddata', 'data.json')
            self.stdout.write('初始数据导入完成！')
        except Exception as e:
            self.stdout.write(f'导入数据时出错: {str(e)}') 