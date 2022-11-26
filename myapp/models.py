from django.db import models

# Create your models here.
class Feature(models.Model):
    name=models.CharField(max_length=100)
    deatils=models.CharField(max_length=500)
    ids= models.IntegerField()