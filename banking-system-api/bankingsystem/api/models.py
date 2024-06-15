from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import BaseUserManager, AbstractUser
import datetime


class Bank(models.Model):
    name = models.CharField(max_length=250)
    bank_id = models.AutoField(primary_key=True)



    def json_object(self):
        return {
            "name": self.name,
            "id": self.bank_id
        }

    def __str__(self):
        return self.name


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    balance = models.IntegerField()
    date_created = models.DateField()
    account_number = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    def json_object(self):
        return {
            "account_id": self.account_id,
            "balance": self.balance,
            "date_created": self.date_created,
            "account_number": self.account_number,
            "password": self.password
        }

    def __str__(self):
        return str(self.account_number)
    
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    CHOICES = [
        ('Withdrawal', 'Withdrawal'),
        ('Deposit', 'Deposit'),
    ]
    transaction_type = models.CharField(max_length=250, choices=CHOICES)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    amount = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    pending = models.BooleanField(default=True)
    def json_object(self):
        return {
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type,
            "timestamp": self.timestamp,
            "amount": self.amount,
            "account": self.account.json_object()
        }

    def __str__(self):
        return str(f"{self.transaction_id}, {self.transaction_type}")
    
    
    

