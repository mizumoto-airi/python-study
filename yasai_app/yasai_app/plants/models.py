from django.db import models

class Plant(models.Model):
    name = models.CharField(max_length=30)        # 野菜の名前
    season = models.CharField(max_length=50)       # 育てる季節
    sow_month = models.IntegerField()              # 種まきの月
    harvest_month = models.IntegerField()          # 収穫の月
    days_to_harvest = models.IntegerField()        # 収穫までの日数
    memo = models.TextField(blank=True)            # メモ（空でもOK）
    created_at = models.DateTimeField(auto_now_add=True)  # 登録日時

    def __str__(self):
        return self.name