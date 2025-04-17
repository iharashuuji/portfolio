import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # プロジェクト名.settings に変更
django.setup()
from logs.models import Log

import pandas as pd
# import matplotlib.pyplot as plt

logs = Log.objects.all().values()
df = pd.DataFrame(logs)

print(df.head(5))