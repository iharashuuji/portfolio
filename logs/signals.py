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
    writer.writerow([
    'id',
    'new_item_today',
    'schedule_changed_today',
    'emotion_state_today',
    'routine_destination_tomorrow',
    'special_event_tomorrow',
    'extra_items_needed_tomorrow',
    'time_difference_tomorrow',
    'will_forget'
])

    for log in logs:
        writer.writerow([
        log.id,
        log.new_item_today,
        log.schedule_changed_today,
        log.emotion_state_today,
        log.routine_destination_tomorrow,
        log.special_event_tomorrow,
        log.extra_items_needed_tomorrow,
        log.time_difference_tomorrow,
        log.will_forget
    ])