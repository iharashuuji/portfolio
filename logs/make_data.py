import os
import django
import random
import numpy as np
import pandas as pd
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# 以下だとデータに方より出ず、
# リアルなデータとの合理性が合わない為、
# ルールベースでデータ作成を行う。
# 以下だとデータにリアル感がないため、ルールベースでデータ作成を行う。

from logs.models import Log

importance_values = np.random.normal(loc=3, scale=1, size=300)
import_values = np.clip(np.round(importance_values), 1, 5).astype(int)

logs = []
for i in range(300):
    # 昨日の情報を基にしたランダムな変動を作成
    # 昨日に関する情報
    new_item_today = random.choice(range(0, 2))  # 新しい物を持っていったか？
    schedule_changed_today = random.choice(range(0, 2))  # 昨日スケジュールに変更があったか？
    
    # 昨日のスケジュール変更が感情に影響を与えるルール
    if schedule_changed_today == 1:
        # 昨日突然スケジュール変更があった場合、今日は疲れた、忙しい、または寝坊した感情が増える
        emotion_state_today = random.choice(['busy', 'late'])
    else:
        # スケジュール変更がなければ、落ち着いた状態が優先される
        emotion_state_today = random.choice(['calm', 'late'])

    # 昨日持っていた物が今日の感情や行動に影響を与える可能性
    if new_item_today == 1:  # 昨日新しい物を持っていた
        emotion_state_today = random.choice(['busy', 'late'])  # 忙しく、焦る感じになるかもしれない

    # 翌日の予定
    routine_destination_tomorrow = random.choice(range(0, 2))  # 明日いつも通りの場所か？
    special_event_tomorrow = random.choice(range(0, 2))  # 明日特別な予定があるか？
    extra_items_needed_tomorrow = random.choice(range(0, 2))  # 明日追加で持っていく物があるか？
    time_difference_tomorrow = random.choice(range(0, 2))  # 通常と異なる時間帯に出発するか？

    # 忘れ物の確率を設定（ルールベース）
    forget_probability = 0.1  # 基本的な忘れ物確率

    # 各カラムの影響を加味する
    if emotion_state_today == '疲労困憊' or emotion_state_today == 'late':
        forget_probability += 0.3  # 疲れている、または焦っていると忘れ物確率が高くなる

    if new_item_today == 1:  # 新しい物を持っていった場合
        forget_probability += 0.2  # 新しい物を持っていくことで、準備に手間取る可能性がある

    if schedule_changed_today == 1:  # 昨日スケジュール変更があった場合
        forget_probability += 0.2  # 変更に慣れていないため、忘れ物が増える

    if extra_items_needed_tomorrow == 1:  # 明日追加の持ち物がある場合
        forget_probability += 0.2  # 追加の持ち物が必要だと、準備が忙しくなり忘れ物のリスクが増える

    if time_difference_tomorrow == 1:  # 明日異なる時間に出発する場合
        forget_probability += 0.2  # 異なる時間に出発することで焦りが生じ、忘れ物確率が上がる

    # 忘れ物をする確率をランダムに決定
    will_forget = 1 if random.random() < forget_probability else 0  # 忘れ物をするか？

    log = Log(
        new_item_today=new_item_today,  # 新しい物を持っていったか
        schedule_changed_today=schedule_changed_today,  # スケジュールに変更があったか
        emotion_state_today=emotion_state_today,  # 今日の感情状態
        routine_destination_tomorrow=routine_destination_tomorrow,  # 明日の予定
        special_event_tomorrow=special_event_tomorrow,  # 特別な予定があるか
        extra_items_needed_tomorrow=extra_items_needed_tomorrow,  # 明日持っていく物があるか
        time_difference_tomorrow=time_difference_tomorrow,  # 明日の出発時間
        will_forget=will_forget,  # 忘れ物したか
    )
    
    logs.append(log)

Log.objects.bulk_create(logs)  # データベースに一括登録