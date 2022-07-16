from django.db import models
from django.contrib.auth.models import Group
from django.contrib.postgres.fields import ArrayField

class Case (models.Model):
    name = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)
    workersList = models.CharField(blank=True, max_length=50)
    workerGroup = models.CharField(max_length=50)
    data = models.TextField(max_length=255)
    description = models.TextField(max_length=255)

    def __str__(self):
        return self.name


