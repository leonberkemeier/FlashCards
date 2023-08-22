from statistics import mode
from unittest.util import _MAX_LENGTH
from django.db import models
from datetime import date

# Create your models here.

class ProjectItem(models.Model):
    created_at=models.DateField(default=date.today)
    name=models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    # project_image = models.ImageField(null=True,blank=True,)

    def __str__(self):
        return str(self.id) + '' + self.name

class Card(models.Model):
    title = models.CharField(max_length=100)
    front = models.FileField(upload_to='Cards/front/')
    back = models.FileField(upload_to='Cards/back/')
    side = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title