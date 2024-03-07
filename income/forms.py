# forms.py
from django import forms
from .models import Income, RecurringIncome, VariedRecurringIncome


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'day_of_month', 'description']
        labels = {'source': 'Income Source', 'day_of_month': 'Credit Day'}
        help_texts = {'day_of_month': 'Specify the day of the month for the income'}
        widgets = {
            'source': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Source Name"}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'day_of_month': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        initial = {'source': 'Source Name', 'recurring_day': 'Select'}


class RecurringIncomeForm(forms.ModelForm):
    class Meta:
        model = RecurringIncome
        fields = ['recurring_type', 'recurring_day', 'recurring_range']
        labels = {'recurring_type': 'Recurring Type', 'recurring_day': 'Recurring Day', 'recurring_range': 'Recurring Range'}
        help_texts = {'recurring_day': 'On which day the income will recur',
                      'recurring_range': 'Specify how many times this income will recur'}
        widgets = {
            'recurring_type': forms.Select(attrs={'class': 'form-control', 'placeholder': "Select"}),
            'recurring_day': forms.Select(attrs={'class': 'form-control', 'placeholder': "Select"}),
            'recurring_range': forms.TextInput(attrs={'class': 'form-control'}),
        }
        initial = {'recurring_type': 'Select', 'recurring_day': 'Select'}


class VariedRecurringIncomeForm(forms.ModelForm):
    class Meta:
        model = VariedRecurringIncome
        fields = ['variation_type', 'variation_amount', 'variation_percentage', 'variation_period', 'variation_description']
        labels = {
            'variation_type': 'Variation Type',
            'variation_amount': 'Variation Amount',
            'variation_percentage': 'Variation Percentage',
            'variation_period': 'Variation Period',
            'variation_description': 'Variation Description',
        }
        help_texts = {
            'variation_amount': 'Specify the amount for the variation',
            'variation_percentage': 'Specify the percentage for the variation',
            'variation_period': 'Specify the period for the variation',
            'variation_description': 'Provide a description for the variation',
        }
        widgets = {
            'variation_type': forms.Select(attrs={'class': 'form-control'}),
            'variation_amount': forms.TextInput(attrs={'class': 'form-control'}),
            'variation_percentage': forms.TextInput(attrs={'class': 'form-control'}),
            'variation_period': forms.TextInput(attrs={'class': 'form-control'}),
            'variation_description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class IncomeTypeForm(forms.Form):
    recurring_type = forms.BooleanField(required=False, initial=False)
    variation_type = forms.BooleanField(required=False, initial=False)
    class Meta:
        prefix = ''  # Set prefix to an empty string to remove it