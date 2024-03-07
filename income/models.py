from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    source = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    day_of_month = models.PositiveIntegerField()

    class Meta:
        ordering = ['day_of_month']

    def __str__(self):
        return f' {self.source} {self.description}'

@receiver(post_save, sender=Income)
def update_related_tables(sender, instance, **kwargs):
    # Update RecurringIncome when Income is saved
    recurring_income = RecurringIncome.objects.filter(income=instance)
    for ri in recurring_income:
        ri.recurring_day = instance.day_of_month
        ri.save()

    # Update VariedRecurringIncome when Income is saved
    varied_recurring_income = VariedRecurringIncome.objects.filter(re_income__income=instance)
    for vri in varied_recurring_income:
        vri.update_variation_fields()
        vri.save()

class RecurringIncome(models.Model):
    RECURRENCE_TYPE_CHOICES = [
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('QM', 'Quarterly Monthly'),
        ('HY', 'Half-Yearly'),
        ('Y', 'Yearly'),
    ]
    DAY_CHOICES = [(i, str(i)) for i in range(1, 31)]  # Choices from 1 to 30
    HOWMANYTINME = [(i, str(i)) for i in range(1, 180)]  # Choices from 1 to 180

    income = models.OneToOneField(Income, on_delete=models.CASCADE, primary_key=True)
    recurring_type = models.CharField(max_length=2, choices=RECURRENCE_TYPE_CHOICES)
    recurring_day = models.PositiveIntegerField(choices=DAY_CHOICES, help_text="On which Day you will get it")
    recurring_range = models.PositiveIntegerField(choices=HOWMANYTINME, help_text="Specify how many times this income will recur.")

    def __str__(self):
        return f'Recurring Income - {self.income.source} - {self.get_recurring_type_display()} - Day {self.recurring_day}'
class VariedRecurringIncome(models.Model):
    re_income = models.OneToOneField(RecurringIncome, on_delete=models.CASCADE, primary_key=True)

    VARIATION_TYPE_CHOICES = [
        ('A', 'Amount'),
        ('P', 'Percentage'),
    ]

    variation_type = models.CharField(max_length=1, choices=VARIATION_TYPE_CHOICES, blank=True, null=True)
    variation_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    variation_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    variation_period = models.PositiveIntegerField(blank=True, null=True)
    variation_description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Varied Recurring Income - {self.re_income}'

    def update_variation_fields(self):
        if self.variation_type == 'P':
            if self.variation_percentage is not None:
                self.variation_amount = (self.re_income.income.amount * self.variation_percentage) / 100
        elif self.variation_type == 'A':
            if self.variation_amount is not None:
                self.variation_percentage = (self.variation_amount / self.re_income.income.amount) * 100

        self.save()