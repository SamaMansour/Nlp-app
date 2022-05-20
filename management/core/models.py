from django.db import models
from django.contrib.postgres.fields import ArrayField
 
class Case (models.Model):
    id =models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    owner = models.CharField(max_length=50)
    workersList = ArrayField(
        models.CharField(max_length=10, blank=True),
        size=8,
    ),
    workerGroup = models.CharField(blank=True,max_length=50)
    data = models.TextField(max_length=255)

