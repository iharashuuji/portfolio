from django.db import models
from logs.models import Log as LogModel
from django.utils.timezone import now


def get_today_log():
    today = now().date()
    # 今日の日付に一致するLogがあれば取得、なければ作成
    log, created = LogModel.objects.get_or_create(date=today)
    return log
# Create your models here.
# class List(models.Model):
#   must_item_1 = models.CharField(max_length=100)
#   must_item_2 = models.CharField(max_length=100)
#   must_item_3 = models.CharField(max_length=100)
#   must_item_4 = models.CharField(max_length=100)
#   must_item_5 = models.CharField(max_length=100)
#   must_item_6 = models.CharField(max_length=100)
#   log = models.ForeignKey(
#         LogModel,
#         on_delete=models.CASCADE, 
#         related_name="suggestions",
#         default=get_today_log )
  
  
from datetime import timedelta
from datetime import date 



  
# ＴｏＤＯＩＴＥＭをまとめるためのもの
class TodoList(models.Model):
  title = models.CharField(max_length=100)
  date = models.DateField(default=date.today)
  log = models.ForeignKey(
        LogModel,
        on_delete=models.CASCADE,
        related_name="list_suggestions",
        )
  created_at = models.DateTimeField(auto_now_add=True)
  
  
class TodoItem(models.Model):
  list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='items')
  task = models.CharField(max_length=255)
  is_done = models.BooleanField(default=False)
  due_date = models.DateField(null=True, blank=True)


