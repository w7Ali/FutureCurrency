# income/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.models import Sum
from .models import Income, RecurringIncome, VariedRecurringIncome
from .forms import (
    IncomeForm,
    RecurringIncomeForm,
    VariedRecurringIncomeForm,
    IncomeTypeForm,
)
from django.contrib import messages

def get_recurring_income_details(income):
    recurring_income = (
        RecurringIncome.objects.get(income=income)
        if hasattr(income, 'recurringincome')
        else None
    )
    varied_recurring_income = (
        VariedRecurringIncome.objects.get(
            re_income=recurring_income
        )
        if recurring_income and hasattr(recurring_income, 'variedrecurringincome')
        else None
    )
    return recurring_income, varied_recurring_income


def get_all_income_details():
    incomes = Income.objects.all()
    income_details = []

    for income in incomes:
        recurring_income, varied_recurring_income = get_recurring_income_details(
            income
        )

        income_detail = {
            'income': income,
            'recurring_income': recurring_income,
            'varied_recurring_income': varied_recurring_income,
        }

        income_details.append(income_detail)

    return income_details


def show_income(request):
    all_income = Income.objects.all()
    total_amount = all_income.aggregate(Sum('amount'))['amount__sum']
    return render(request, 'income/home.html', {'all_income': all_income, 'total_amount': total_amount})

def create_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Added Successfully")
    else:
        form = IncomeForm()

    return render(request, 'income/add-income.html', {'form': form})

def edit_income(request, income_id):
    income = get_object_or_404(Income, id=income_id)

    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income_home')
    else:
        form = IncomeForm(instance=income)

    return render(request, 'income/edit-income.html', {'form': form, 'income': income})

def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id)

    if request.method == 'POST':
        try:
            income.delete()
            return redirect('income_home')
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

    return HttpResponseBadRequest("Invalid Request")

def delete_selected_income(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')

        try:
            Income.objects.filter(id__in=selected_items).delete()
            return redirect('income_home')
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

    return HttpResponseBadRequest("Invalid Request")

def all_create_income(request):
    if request.method == 'POST':
        income_form = IncomeForm(request.POST)
        recurring_income_form = RecurringIncomeForm(request.POST)
        varied_recurring_income_form = VariedRecurringIncomeForm(request.POST)
        income_type_form = IncomeTypeForm(request.POST)

        if income_form.is_valid() and income_type_form.is_valid():
            income = income_form.save()

            if income_type_form.cleaned_data['recurring_type']:
                if recurring_income_form.is_valid():
                    recurring_income = recurring_income_form.save(commit=False)
                    recurring_income.income = income
                    recurring_income.save()

                    if (
                        income_type_form.cleaned_data['variation_type']
                        and varied_recurring_income_form.is_valid()
                    ):
                        varied_recurring_income = varied_recurring_income_form.save(
                            commit=False
                        )
                        varied_recurring_income.re_income = recurring_income
                        varied_recurring_income.save()

                return redirect('income_home')  # Redirect to a success page

            return redirect('income_home')  # Redirect to a success page

    else:
        income_form = IncomeForm()
        recurring_income_form = RecurringIncomeForm()
        varied_recurring_income_form = VariedRecurringIncomeForm()
        income_type_form = IncomeTypeForm()

    return render(
        request,
        'income/add-income.html',
        {
            'income_form': income_form,
            'recurring_income_form': recurring_income_form,
            'varied_recurring_income_form': varied_recurring_income_form,
            'income_type_form': income_type_form,
        },
    )

def view_income_details(request):
    income_details = get_all_income_details()
    return render(request, 'income/home.html', {'income_details': income_details})

def get_income_details(request, income_id):
    # Get the Income object with the specified id
    income = Income.objects.get(id=income_id)

    # Get related RecurringIncome object if it exists
    recurring_income = RecurringIncome.objects.filter(income=income).first()

    # Get related VariedRecurringIncome object if it exists
    varied_recurring_income = (
        VariedRecurringIncome.objects.filter(
            re_income__income=income
        ).first()
    )

    # Construct the dictionary
    all_income = {
        'income': {
            'id': income.id,
            'amount': income.amount,
            'source': income.source,
            'description': income.description,
            'day_of_month': income.day_of_month,
        },
        'recurring_income': None,
        'varied_recurring_income': None,
    }

    if recurring_income:
        all_income['recurring_income'] = {
            'recurring_type': recurring_income.recurring_type,
            'recurring_day': recurring_income.recurring_day,
            'recurring_range': recurring_income.recurring_range,
        }

    if varied_recurring_income:
        all_income['varied_recurring_income'] = {
            'variation_type': varied_recurring_income.variation_type,
            'variation_amount': varied_recurring_income.variation_amount,
            'variation_percentage': varied_recurring_income.variation_percentage,
            'variation_period': varied_recurring_income.variation_period,
            'variation_description': varied_recurring_income.variation_description,
        }

    return render(
        request, 'income/income-detail.html', {'all_income': all_income}
    )
