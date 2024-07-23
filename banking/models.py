from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfiles(models.Model):
    UP_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    UP_UserName = models.CharField(max_length=200, null=True, blank=True)
    UP_UserAdress = models.CharField(max_length=10000, null=True, blank=True)
    UP_email = models.EmailField(null=True, blank=True)
    UP_contact = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return str(self.UP_UserName)
    
class Account(models.Model):
    AC_type = (
        ('Savings', 'Savings'),
        ('Current', 'Current'),
    )
    AC_user = models.OneToOneField(UserProfiles, on_delete=models.CASCADE, null=True, blank=True)
    AC_Creation_date = models.DateTimeField(auto_now_add=True)
    AC_AccoutNumber = models.CharField(max_length=20, default='000000000000', null=True, blank=True)
    AC_AccoutType = models.CharField(max_length=20, choices=AC_type, default='Savings', null=True, blank=True)
    AC_balance = models.FloatField(default=0)

    def __str__(self):
        return str(self.AC_user.UP_UserName)

class Transactions(models.Model):
    TC_sender_account = models.ForeignKey(Account, related_name='sent_transactions',on_delete=models.CASCADE ,null=True, blank=True)
    TC_amount = models.CharField(max_length=50, null=True, blank=True)
    TC_type = models.CharField(max_length=100, null=True, blank=True)
    TC_date = models.DateTimeField(auto_now_add=True)
    TC_receiver_account = models.ForeignKey(Account, related_name='received_transactions' ,on_delete=models.CASCADE ,null=True, blank=True)

    def __str__(self):
        return str(self.TC_date) + ' ' + str(self.TC_sender_account.AC_user.UP_UserName)