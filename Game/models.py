from django.db import models

class Char(models.Model):
    name = models.CharField(max_length=100)
    life = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    job = models.CharField(max_length=50, default='default_value')



