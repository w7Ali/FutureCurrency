# models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.contrib.auth.models import User


class Expense(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Expense - {self.amount} on {self.date}'

class Emi(models.Model):

    DAY_CHOICES = [(i, str(i)) for i in range(1, 31)]
    HOWMANYTINME = [(i, str(i)) for i in range(1, 180)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    down_payment = models.DecimalField(max_digits=10, decimal_places=2)
    emi_amount = models.IntegerField()
    start_date = models.DateField()
    due_date = models.PositiveIntegerField(choices=DAY_CHOICES, help_text="On which Day it will get Debit")
    emi_count = models.PositiveIntegerField(choices=HOWMANYTINME, help_text="Number Of Total EMI.")
    interest_percent = models.DecimalField(max_digits=5, decimal_places=2, help_text="Interest percentage")

    def __str__(self):
        return f'{self.product_name} - EMI'

class EmiBalance(models.Model):
    emi = models.OneToOneField(Emi, on_delete=models.CASCADE)
    paid_amount = models.IntegerField(default=0)
    remaining_emis = models.PositiveIntegerField(default=0)
    pending_amount = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)

    def calculate_balance(self):
        today = datetime.today().date()
        start_month = self.emi.start_date.month
        start_year = self.emi.start_date.year
        paid_amount = 0

        for year in range(start_year, today.year + 1):
            start = start_month if year == start_year else 1
            end = today.month if year == today.year else 12

            for month in range(start, end + 1):
                paid_amount += self.emi.emi_amount

        # Check if the due day is already passed for the current month
        if today.day > self.emi.due_date:
            paid_amount += self.emi.emi_amount

        self.paid_amount = paid_amount

        remaining_emis = self.emi.emi_count - (paid_amount // self.emi.emi_amount)
        self.remaining_emis = max(0, remaining_emis)

        remaining_months = (self.emi.start_date.year - today.year) * 12 + self.emi.start_date.month - today.month
        if today.day > self.emi.due_date:
            remaining_months -= 1

        remaining_emis += remaining_months
        self.pending_amount = max(0, remaining_emis * self.emi.emi_amount)

        # Calculate total amount
        self.total_amount = self.emi.emi_amount * self.emi.emi_count

        self.save()

    def calculate_interest(self):
        # Assuming interest is calculated based on the pending amount
        interest_amount = (self.pending_amount * self.emi.interest_percent) / 100
        return interest_amount

    def __str__(self):
        return f'EmiBalance for {self.emi.product_name}'

@receiver(post_save, sender=Emi)
def create_or_update_emi_balance(sender, instance, created, **kwargs):
    if created:
        EmiBalance.objects.create(emi=instance)
    else:
        instance.emibalance.calculate_balance()

# Connect the signal
post_save.connect(create_or_update_emi_balance, sender=Emi)