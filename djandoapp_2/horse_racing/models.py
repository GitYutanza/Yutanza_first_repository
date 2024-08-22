# horse_scraper/models.py

from django.db import models

class RaceResult(models.Model):
    race_id = models.CharField(max_length=20)
    horse_name = models.CharField(max_length=255)
    jockey_name = models.CharField(max_length=255)
    horse_number = models.IntegerField()
    runtime = models.CharField(max_length=50, blank=True, null=True)
    odds = models.FloatField()
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
    race_date = models.DateField()
    track = models.CharField(max_length=50)
    race_class = models.CharField(max_length=50)
    surface = models.CharField(max_length=50)
    distance = models.IntegerField()
    turn = models.CharField(max_length=50)
    track_condition = models.CharField(max_length=50)
    weather = models.CharField(max_length=50)
    track_id = models.IntegerField()
    track_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.race_name} - {self.horse_name} - Position {self.position}"

