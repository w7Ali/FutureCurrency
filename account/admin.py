from django.contrib import admin
from .models import Account
# Register your models here.
@admin.register(Account)
class AdminAccount(admin.ModelAdmin):
    list_display = ('account_name', 'account_number', 'balance')