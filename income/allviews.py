# # forms.py
# from django.forms import forms
# from .views import *
# class IncomeForm(forms.ModelForm):
#     class Meta:
#         model = Income
#         fields = ['amount', 'source', 'description', 'day_of_month']
#
# class RecurringIncomeForm(forms.ModelForm):
#     class Meta:
#         model = RecurringIncome
#         fields = ['recurring_type', 'recurring_day', 'recurring_range']
#
# class VariedRecurringIncomeForm(forms.ModelForm):
#     class Meta:
#         model = VariedRecurringIncome
#         fields = ['variation_type', 'variation_amount', 'variation_percentage', 'variation_period', 'variation_description']
#
# # views.py
# from django.shortcuts import render, redirect
# from .forms import IncomeForm, RecurringIncomeForm, VariedRecurringIncomeForm
#
# def alladd_income(request):
#     if request.method == 'POST':
#         income_form = IncomeForm(request.POST)
#         recurring_income_form = RecurringIncomeForm(request.POST)
#         varied_recurring_income_form = VariedRecurringIncomeForm(request.POST)
#
#         if income_form.is_valid() and recurring_income_form.is_valid() and varied_recurring_income_form.is_valid():
#             # Save the Income model
#             income = income_form.save()
#
#             # Save the RecurringIncome model
#             recurring_income = recurring_income_form.save(commit=False)
#             recurring_income.income = income
#             recurring_income.save()
#
#             # Save the VariedRecurringIncome model
#             varied_recurring_income = varied_recurring_income_form.save(commit=False)
#             varied_recurring_income.re_income = income.recurringincome
#             varied_recurring_income.save()
#
#             return redirect('IncomeHome')
#     else:
#         income_form = IncomeForm()
#         recurring_income_form = RecurringIncomeForm()
#         varied_recurring_income_form = VariedRecurringIncomeForm()
#
#     return render(request, 'core/income_form.html', {'income_form': income_form, 'recurring_income_form': recurring_income_form, 'varied_recurring_income_form': varied_recurring_income_form})
