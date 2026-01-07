from django.db import models

# Create your models here.
from django.db import models


class Plan(models.Model):
    
    Type = models.CharField(max_length = 20)
    StartDate = models.DateField()
    Duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
