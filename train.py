import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # プロジェクト名.settings に変更
django.setup()
from logs.models import Log

import pandas as pd
# import matplotlib.pyplot as plt

logs = Log.objects.all().values()
df = pd.DataFrame(logs)

# 機械学習データの用意、データクレンジング
x = df.drop(['id','forget_count'], axis=1)
y = df['forget_count']



# 以下にするべき分析を記載を行う
# FORGOTCOUNTの予想
# その予測にどのような変数が関わったかを記載を行う。
# 予測に使う変数を選択

# カラム名：['id', 'forgotten_item_place', 'frequency', 'importance',
# 'recovery_difficulty', 'size', 'weight', 'visibility', 'forget_count','time_prone', 'emotion_state']


# 137 is the number of 1, 163 is the number of 0 →不均衡データでもない
# 欠損数を確認 →無し

