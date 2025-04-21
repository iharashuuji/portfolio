from django.db import models
import datetime

class Log(models.Model):
    # 前日の状態
    # 新しいものを今日持っているか？
    date = models.DateField(unique=True, default=datetime.date.today)

    new_item_today = models.BooleanField()  # 新しい物を持っていったか
    # 今日は突然のスケジュールが会ったか？
    schedule_changed_today = models.BooleanField()  # スケジュールに変更があったか
    # 焦っていたなどの感情はあるか？
    emotion_state_today = models.CharField(
        max_length=10,
        choices=[
            ('calm', '落ち着いている'),
            ( 'busy','忙しい'),
            ('late', '寝坊した')
        ],

    )
    # 翌日の予定
    # 明日はいつもの場所に行くか
    routine_destination_tomorrow = models.BooleanField()  # いつも通りの場所か
    # 明日特別な予定があるか
    special_event_tomorrow = models.BooleanField()  # 特別な予定があるか
    # 明日は追加の持ち物があるか
    extra_items_needed_tomorrow = models.BooleanField()  # 追加で持っていく物があるか
    # 明日はいつもと違う時間に出発するか
    time_difference_tomorrow = models.BooleanField()  # 通常と異なる時間帯か

    # 目的変数
    will_forget = models.BooleanField(null=True, blank=True, default=None)  # 翌日に忘れ物をするか