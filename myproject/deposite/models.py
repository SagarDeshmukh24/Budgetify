from django.db import models

# Create your models here.
class Deposite(models.Model):
    deposite_id = models.CharField(max_length= 10, unique=True)
    type = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.type

