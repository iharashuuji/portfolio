import os 
import django
import random
import numpy as np
from .signals import logs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from logs.models import Log

FREQUENCY_CHOICES = ['daily', 'weekly', 'monthly', 'once']
RECOVERY_DIFFICULTY_CHOICES = ['easy', 'medium', 'hard']
SIZE_CHOICES = ['small', 'medium', 'large']
WEIGHT_CHOICES = ['light', 'normal', 'heavy']
VISIBILITY_CHOICES = [True, False]
TIME_PRONE_CHOICES = ['morning', 'noon', 'night']
EMOTION_STATE_CHOICES = ['busy', 'late', 'calm']

importance_values = np.random.normal(loc=3, scale=1, size=300)
import_values = np.clip(np.round(importances_values), 1, 5).astype(int)

for i in range(300):
    log = Log(
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
    
