from django.db import models
from logs.models import Log as LogModel
from django.utils.timezone import now
from datetime import timedelta
from datetime import date 

  
# ＴｏＤＯＩＴＥＭをまとめるためのもの
class List(models.Model):
  # title = models.CharField(max_length=100)
  date = models.DateField(default=date.today, unique=True)
  # log = models.ForeignKey(
  #       LogModel,
  #       on_delete=models.CASCADE,
  #       related_name="list_suggestions",
  #       )
  created_at = models.DateTimeField(auto_now_add=True)
  
  
class Item(models.Model):
  list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='items')
  task = models.CharField(max_length=255)
  proposal = models.TextField(null=True, blank=True)
  is_done = models.BooleanField(default=False)
  due_date = models.DateField(null=True, blank=True)


