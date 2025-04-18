import os 
import django
import random
import numpy as np
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()


# 以下だとデータに方より出ず、
# リアルなデータとの合理性が合わない為、
# ルールベースでデータ作成を行う。

# 以下にルールを記載を行う。
# 1. 


from logs.models import Log

FREQUENCY_CHOICES = ['daily', 'weekly', 'monthly', 'once']
FORGATTON_CHOICES = [True, False]
RECOVERY_DIFFICULTY_CHOICES = ['easy', 'medium', 'hard']
SIZE_CHOICES = ['small', 'large']
WEIGHT_CHOICES = ['light', 'heavy']
VISIBILITY_CHOICES = [True, False]
TIME_PRONE_CHOICES = ['morning', 'noon', 'night']
EMOTION_STATE_CHOICES = ['busy', 'late', 'calm']

importance_values = np.random.normal(loc=3, scale=1, size=300)
import_values = np.clip(np.round(importance_values), 1, 5).astype(int)

logs = []
for i in range(300):
    log = Log(
        forget_count = random.choice(range(0,2)),
        forgotten_item_place=random.choice(FORGATTON_CHOICES),
        frequency=random.choice(FREQUENCY_CHOICES),
        importance=importance_values[i],
        recovery_difficulty=random.choice(RECOVERY_DIFFICULTY_CHOICES),
        size=random.choice(SIZE_CHOICES),
        weight=random.choice(WEIGHT_CHOICES),
        visibility=random.choice(VISIBILITY_CHOICES),
        time_prone=random.choice(TIME_PRONE_CHOICES),
        emotion_state=random.choice(EMOTION_STATE_CHOICES),
    )
    logs.append(log)
    
    
Log.objects.bulk_create(logs)
