from django.contrib import admin
from .models import Income, RecurringIncome, VariedRecurringIncome
# Register your models here.
@admin.register(Income)
class IncomAdmin(admin.ModelAdmin):
    list_display = ('id','amount','source','description','day_of_month')


@admin.register(RecurringIncome)
class RecussingAdmin(admin.ModelAdmin):
    list_display = ('income','recurring_type','recurring_day','recurring_range')

@admin.register(VariedRecurringIncome)
class VariedAdmin(admin.ModelAdmin):
    list_display = ('re_income','variation_type','variation_amount','variation_percentage','variation_period','variation_description')

