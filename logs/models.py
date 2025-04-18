from django.db import models

class Log(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', '毎日'),('weekly', '週1'),('monthly', '月1'),('once', '今回だけ')
    ]

    IMPORTANCE_CHOICES = [
        (1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
    ]

    RECOVERY_DIFFICULTY_CHOICES = [
        ('easy', '買い直せる'),('medium', '家に戻ればなんとかなる'),('hard', '代用不可')
    ]

    SIZE_CHOICES = [
        ('small', '小'),('large', '大')
    ]

    WEIGHT_CHOICES = [
        ('light', '軽い'),('heavy', '重い')
    ]

    VISIBILITY_CHOICES = [
        (True, '目立つ'),(False, '目立ちにくい')
    ]

    TIME_PRONE_CHOICES = [
        ('morning', '朝'),('noon', '昼'),('night', '夜')
    ]

    EMOTION_STATE_CHOICES = [
        ('busy', '慌ただしい'),('late', '寝坊した'),('calm', '落ち着いている')
    ]

    forgotten_item_place = models.BooleanField(null=True) 

    frequency = models.CharField(null=True,max_length=20, choices=FREQUENCY_CHOICES)

    importance = models.IntegerField(null=True,choices=IMPORTANCE_CHOICES)
    recovery_difficulty = models.CharField(max_length=50, choices=RECOVERY_DIFFICULTY_CHOICES)
    


    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    weight = models.CharField(max_length=10, choices=WEIGHT_CHOICES)
    visibility = models.BooleanField(choices=VISIBILITY_CHOICES, default=True)
    
    forget_count = models.IntegerField(null=True,default=0) 
    time_prone = models.CharField(max_length=10,null=True, choices=TIME_PRONE_CHOICES, blank=True)  
    emotion_state = models.CharField(max_length=30,null=True, choices=EMOTION_STATE_CHOICES, blank=True)  


