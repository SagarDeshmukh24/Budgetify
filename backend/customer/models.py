from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length= 10)
    password = models.CharField(max_length=20, default='')
    type = models.CharField(max_length=50, default='')
    reset_otp = models.IntegerField(null=True, blank=True)
    telegram_chat_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
