# # Models
from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
#
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.account_name} - {self.user.username}'
#
# @receiver(post_save, sender=User)
# def create_user_account(sender, instance, created, **kwargs):
#     if created:
#         Account.objects.create(user=instance, account_name=f'{instance.username} Account')
#
# # Connect the signal
# post_save.connect(create_user_account, sender=User)
