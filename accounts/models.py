# from django.db import models

# # Create your models here.


from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    holder_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.account_number} - {self.holder_name}"

# class Transaction(models.Model): # Note: use standard colon
#     # Fix syntax for model below:
#     # pass
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)
#     transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')])
#     amount = models.DecimalField(max_digits=12, decimal_places=2)

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.timestamp}"
