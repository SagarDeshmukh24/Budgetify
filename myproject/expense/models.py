from django.db import models
from datetime import date

class Expense(models.Model):

    # EXPENSE_CHOICES = [
    #     ('money_transfer', 'Money Transfer'),
    #     ('food', 'Food'),
    #     ('fuel', 'Fuel'),
    #     ('grocery', 'Grocery'),
    #     ('medical', 'Medical'),
    #     ('other', 'Other'),
    #     ('investment', 'Investment'),
    #     ('education', 'Education'),
    #     ('travel', 'Travel'),
    #     ('bill_payment', 'Bill Payment'),
    # ]

    expense_id = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length= 50)
    description = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.type