from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Log
import csv
import os
from django.conf import settings

@receiver(post_save, sender=Log)
def export_log_to_csv(sender, instance, **kwargs):
  # sender は、どのモデルに反応するかを記述 
  # 保存されたら、記述
  filepath = os.path.join(settings.MEDIA_ROOT, 'exports', 'logs.csv')
  os.makedirs(os.path.dirname(filepath), exist_ok=True)
  # CSVを保存するパスを作成
  logs = Log.objects.all()
  with open(filepath, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id',  'usage_date', 'usage_time',  'frequency', 'last_used_date', 'importance', 'recovery_difficulty', 'size', 'weight', 'visibility', 'forget_count', 'time_prone', 'emotion_state'])
    for log in logs:
      writer.writerow([log.id,  log.usage_date, log.usage_time,  log.frequency, log.last_used_date, log.importance, log.recovery_difficulty, log.size, log.weight, log.visibility, log.forget_count, log.time_prone, log.emotion_state])