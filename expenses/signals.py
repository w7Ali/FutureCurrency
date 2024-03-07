# your_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Emi, EmiBalance

@receiver(post_save, sender=Emi)
def create_or_update_emi_balance(sender, instance, created, **kwargs):
    if created:
        EmiBalance.objects.create(emi=instance)
    else:
        instance.emibalance.calculate_balance()

# Connect the signal
post_save.connect(create_or_update_emi_balance, sender=Emi)
