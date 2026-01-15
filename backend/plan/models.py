from django.db import models

# Create your models here.
from django.db import models


class Plan(models.Model):
    
    type = models.CharField(max_length = 20)
    duration = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.type