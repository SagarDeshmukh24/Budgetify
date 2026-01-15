from django.db import models
from customer.models import Customer


from django.utils import timezone

# Create your models here.
class Transaction(models.Model):
    transaction_id = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)

    credit_amt = models.IntegerField(default=0)
    debit_amt = models.IntegerField(default=0)

    description = models.CharField(default="")
    deposite_type = models.CharField(default="other")
    expense_type = models.CharField(default="other")

    customer_id = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="f_customer_id",
        default=0
    )