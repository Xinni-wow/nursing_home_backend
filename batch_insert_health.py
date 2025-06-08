# 批量插入健康记录的脚本
from datetime import date, timedelta
import random
import django
import os

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nursing_home_backend.settings')
django.setup()

from health.models import HealthRecord
from elders.models import Elder

# 获取指定的两位老人
elder_ids = [4, 8]
elders = Elder.objects.filter(id__in=elder_ids)

# 生成近 14 天的数据
today = date.today()
dates = [today - timedelta(days=i) for i in range(30)]

records_to_create = []

for elder in elders:
    for d in dates:
        if HealthRecord.objects.filter(elder=elder, date=d).exists():
            continue

        record = HealthRecord(
            elder=elder,
            date=d,
            temperature=round(random.uniform(36.5, 37.2), 1),  # 正常体温
            blood_pressure_systolic=random.randint(115, 125),  # 更精确的收缩压
            blood_pressure_diastolic=random.randint(75, 80),   # 更精确的舒张压
            heart_rate=random.randint(60, 80),                 # 心率
            blood_sugar=round(random.uniform(4.7, 5.6), 1),    # 血糖
            respiratory_rate=random.randint(16, 18),           # 呼吸频率
            oxygen_saturation=round(random.uniform(97, 99), 1),# 血氧
            weight=round(random.uniform(65.0, 67.0), 1)        # 体重小幅变化
        )
        records_to_create.append(record)


# 批量插入
HealthRecord.objects.bulk_create(records_to_create)

print(f"已为老人ID {elder_ids} 批量添加 {len(records_to_create)} 条健康记录。")
