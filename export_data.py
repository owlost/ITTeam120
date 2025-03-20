import os
import django
import json
import sys

print("开始导出数据...")

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')
django.setup()

print("Django 环境已设置")

from django.core.management import call_command
from django.core.serializers.json import DjangoJSONEncoder

# 设置标准输出为 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

print("开始执行 dumpdata 命令...")

# 导出数据
try:
    # 使用 StringIO 来捕获输出
    from io import StringIO
    output = StringIO()
    call_command('dumpdata', '--exclude', 'auth.permission', '--exclude', 'contenttypes', '--indent', '2', stdout=output)
    
    # 将数据写入文件，使用 UTF-8 编码
    with open('data.json', 'w', encoding='utf-8', newline='') as f:
        f.write(output.getvalue())
    
    print("数据导出成功！")
except Exception as e:
    print(f"导出过程中出现错误: {str(e)}")
    # 打印更详细的错误信息
    import traceback
    traceback.print_exc() 