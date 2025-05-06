import os
import django
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import  f1_score, roc_auc_score


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # プロジェクト名.settings に変更
django.setup()
from proposals.models import List, Item

import pandas as pd
# import matplotlib.pyplot as plt

logs = List.objects.all().values()
df = pd.DataFrame(logs)


df_copy = df_copy.fillna(False)


X = df_copy.drop(columns=['will_forget', 'id'],axis=1)
y = df_copy['will_forget']


# 欠損がない珍しいデータなので、ＲＮＡＤＯＭＦＯＲＥＳＴを用いる。
# 予測モデルの構築
rf = RandomForestClassifier(
  n_estimators=100,
  class_weight='balanced',
  random_state=42,)

# モデルの学習
rf.fit(X_train, y_train)


import joblib
joblib.dump(rf, 'model_pro.pkl')


