from django import forms
from .models import Expense, Emi, EmiBalance

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'class': 'custom-input-class'}),
        }
        help_texts = {
            'date': 'Enter the date in the format DD/MM/YYYY.',
        }


class EmiForm(forms.ModelForm):
    class Meta:
        model = Emi
        fields = '__all__'
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'down_payment': forms.TextInput(attrs={'class': 'form-control'}),
            'emi_amount': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control'}),
            'due_date': forms.Select(attrs={'class': 'form-control'}),
            'emi_count': forms.Select(attrs={'class': 'form-control'}),
            'interest_percent': forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'start_date': 'Enter the start date in the format DD/MM/YYYY.',
        }