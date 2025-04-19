import os
import django
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import  f1_score, roc_auc_score


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # プロジェクト名.settings に変更
django.setup()
from logs.models import Log

import pandas as pd
# import matplotlib.pyplot as plt

logs = Log.objects.all().values()
df = pd.DataFrame(logs)



# データクレンジング
# 機械学習データの用意
df_copy = pd.get_dummies(df.copy(), columns=['emotion_state_today'])



df_copy = df_copy.fillna(False)


X = df_copy.drop(columns=['will_forget', 'id'],axis=1)
y = df_copy['will_forget']



skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for train_index, test_index in skf.split(X, y):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
# 目的変数は、１：０＝数２：１の不均衡データなので、何等かの調節が必要と考えられる。


# 欠損がない珍しいデータなので、ＲＮＡＤＯＭＦＯＲＥＳＴを用いる。
# 予測モデルの構築
rf = RandomForestClassifier(
  n_estimators=100,
  class_weight='balanced',
  random_state=42,)

# モデルの学習
rf.fit(X_train, y_train)

# y_pred = rf.predict(X_test)
# f1_score_value = f1_score(y_test, y_pred)
# roc_auc_score_value = roc_auc_score(y_test, y_pred)

# print(f'F1 Score: {f1_score_value}')
# print(f'ROC AUC Score: {roc_auc_score_value}') 
# 評価指標に関しては、かなり精度が重要になるので、F1, ROUCーAUCを用いる。
import joblib
joblib.dump(rf, 'model.pkl')

# 以下にするべき分析を記載を行う
# FORGOTCOUNTの予想
# その予測にどのような変数が関わったかを記載を行う。
# 予測に使う変数を選択

# カラム名：['id', 'forgotten_item_place', 'frequency', 'importance',
# 'recovery_difficulty', 'size', 'weight', 'visibility', 'forget_count','time_prone', 'emotion_state']


# 137 is the number of 1, 163 is the number of 0 →不均衡データでもない
# 欠損数を確認 →無し
