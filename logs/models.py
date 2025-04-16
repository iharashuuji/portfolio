from django.db import models

class Log(models.Model):
    # 使用頻度の選択肢
    FREQUENCY_CHOICES = [
        ('daily', '毎日'),
        ('weekly', '週1'),
        ('monthly', '月1'),
        ('once', '今回だけ')
    ]

    # 重要度の選択肢（1が最も低く、5が最も高い）
    IMPORTANCE_CHOICES = [
        (1, '1（低）'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5（高）')
    ]

    # 回復の難易度の選択肢
    RECOVERY_DIFFICULTY_CHOICES = [
        ('easy', '買い直せる'),
        ('medium', '家に戻ればなんとかなる'),
        ('hard', '代用不可')
    ]

    # 物のサイズの選択肢
    SIZE_CHOICES = [
        ('small', '小'),
        ('medium', '中'),
        ('large', '大')
    ]

    # 物の重さの選択肢
    WEIGHT_CHOICES = [
        ('light', '軽い'),
        ('normal', '普通'),
        ('heavy', '重い')
    ]

    # 物が目立つかどうか
    VISIBILITY_CHOICES = [
        (True, '目立つ'),
        (False, '目立ちにくい')
    ]

    # 忘れやすい時間帯の選択肢
    TIME_PRONE_CHOICES = [
        ('morning', '朝'),
        ('noon', '昼'),
        ('night', '夜')
    ]

    # 忘れやすい感情状態の選択肢
    EMOTION_STATE_CHOICES = [
        ('busy', '慌ただしい'),
        ('late', '寝坊した'),
        ('calm', '落ち着いている')
    ]

    # 1. 忘れ物の基本情報
    name = models.CharField(max_length=100)  # 忘れ物の名前
    usage_date = models.DateField()          # 使用予定日
    usage_time = models.TimeField()          # 使用予定時刻
    usage_place = models.CharField(max_length=100)  # 使用場所（屋内／屋外など）

    # 2. 使用頻度・習慣
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    last_used_date = models.DateField(null=True, blank=True)  # 最後に使った日

    # 3. 重要度・緊急性
    importance = models.IntegerField(choices=IMPORTANCE_CHOICES)  # 重要度（1〜5）
    recovery_difficulty = models.CharField(max_length=50, choices=RECOVERY_DIFFICULTY_CHOICES)  # 回復の難易度

    # 4. 物理的特徴
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)  # サイズ（小・中・大）
    weight = models.CharField(max_length=10, choices=WEIGHT_CHOICES)  # 重さ（軽い・普通・重い）
    visibility = models.BooleanField(choices=VISIBILITY_CHOICES, default=True)  # 目立つかどうか

    # 5. 行動傾向
    forget_count = models.IntegerField(default=0)  # 何回忘れたか
    time_prone = models.CharField(max_length=10, choices=TIME_PRONE_CHOICES, blank=True)  # 忘れやすい時間帯
    emotion_state = models.CharField(max_length=30, choices=EMOTION_STATE_CHOICES, blank=True)  # 感情状態

    # 6. 忘れ物リマインダー設定（追加機能）
    reminder_set = models.BooleanField(default=False)  # リマインダー設定の有無

    def __str__(self):
        return self.name
