from django.db import models

# Create your models here.
class List(models.Model):
  must_item_1 = models.CharField(max_length=100)
  must_item_2 = models.CharField(max_length=100)
  must_item_3 = models.CharField(max_length=100)
  must_item_4 = models.CharField(max_length=100)
  must_item_5 = models.CharField(max_length=100)
  must_item_6 = models.CharField(max_length=100)