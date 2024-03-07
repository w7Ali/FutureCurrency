from django.contrib import admin
from .models import Expense, Emi, EmiBalance
# Register your models here.

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['amount', 'category', 'description', 'date']

@admin.register(Emi)
class EmiAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'emi_amount', 'start_date', 'due_date', 'emi_count']

@admin.register(EmiBalance)
class EmiBalanceAdmin(admin.ModelAdmin):
    list_display = ['emi', 'paid_amount', 'remaining_emis', 'pending_amount']

