# horse_scraper/models.py

from django.db import models

class MyModelManager(models.Manager):
    def create(self, **kwargs):
        # カスタムロジックを追加する
        try:
            float(kwargs['odds'])
        except:
            kwargs['odds']=None
        else:
            kwargs['odds']=float(kwargs['odds'])

        # オリジナルのcreate()メソッドを呼び出す
        return super().create(**kwargs)

class RaceResult(models.Model):
    race_id = models.CharField(max_length=20)
    horse_name = models.CharField(max_length=255)
    jockey_name = models.CharField(max_length=255)
    horse_number = models.IntegerField()
    runtime = models.CharField(max_length=50, blank=True, null=True)
    odds = models.FloatField(null=True)
    passing_order = models.CharField(max_length=50, blank=True, null=True)
    position = models.IntegerField()
    weight = models.IntegerField()
    weight_change = models.IntegerField()
    sex = models.CharField(max_length=10)
    age = models.IntegerField()
    weight_carry = models.FloatField()
    last_3f = models.CharField(max_length=50, blank=True, null=True)
    popularity = models.CharField(max_length=50, blank=True, null=True)
    race_name = models.CharField(max_length=255)
    race_date = models.DateField(null=True)
    track = models.CharField(max_length=50)
    race_class = models.CharField(max_length=50)
    surface = models.CharField(max_length=50)
    distance = models.IntegerField()
    turn = models.CharField(max_length=50)
    track_condition = models.CharField(max_length=50)
    weather = models.CharField(max_length=50)
    track_id = models.IntegerField()
    track_name = models.CharField(max_length=50)

    objects=MyModelManager()

    def __str__(self):
        return f"{self.race_name} - {self.horse_name} - Position {self.position}"

