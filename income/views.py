from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from core.decorators import login_required_view
from .models import Income, RecurringIncome, VariedRecurringIncome
from .forms import (
    IncomeForm,
    RecurringIncomeForm,
    VariedRecurringIncomeForm,
    IncomeTypeForm,
)


def get_recurring_income_details(income):
    recurring_income = RecurringIncome.objects.filter(income=income).first()
    varied_recurring_income = (
        VariedRecurringIncome.objects.filter(re_income__income=income).first()
        if recurring_income
        else None
    )
    return recurring_income, varied_recurring_income


def get_all_income_details(user):
    incomes = Income.objects.filter(user=user)
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

# @login_required_view
# def edit_income(request, income_id):
#     income = get_object_or_404(Income, id=income_id)

#     if request.method == 'POST':
#         form = IncomeForm(request.POST, instance=income)
#         if form.is_valid():
#             form.save(commit=False)
#             form.user = request.user
#             return redirect('income-home')
#     else:
#         form = IncomeForm(instance=income)

#     return render(request, 'income/edit-income.html', {'form': form, 'income': income})


# @login_required_view
# def deleteincome(request, income_id):
#     income = get_object_or_404(Income, id=income_id)

#     if request.method == 'POST':
#         try:
#             income.delete()
#             return redirect('income-home')
#         except Exception as e:
#             return HttpResponseBadRequest(f"Error: {str(e)}")

#     return HttpResponseBadRequest("Invalid Request")


# @login_required_view
# def delete_selected_income(request):
#     if request.method == 'POST':
#         selected_items = request.POST.getlist('selected_items')

#         try:
#             Income.objects.filter(id__in=selected_items).delete()
#             return redirect('income-home')
#         except Exception as e:
#             return HttpResponseBadRequest(f"Error: {str(e)}")

#     return HttpResponseBadRequest("Invalid Request")

# @login_required_view
# def create_income(request, income_id=None):
#     income = get_object_or_404(Income, id=income_id) if income_id else None
#     recurring_income = RecurringIncome.objects.filter(income=income).first() if income else None
#     varied_recurring_income = (
#         VariedRecurringIncome.objects.filter(re_income__income=income).first()
#         if recurring_income
#         else None
#     )

#     if request.method == 'POST':
#         income_form = IncomeForm(request.POST, instance=income)
#         recurring_income_form = RecurringIncomeForm(request.POST, instance=recurring_income)
#         varied_recurring_income_form = VariedRecurringIncomeForm(
#             request.POST, instance=varied_recurring_income
#         )
#         income_type_form = IncomeTypeForm(request.POST)

#         if income_form.is_valid():
#             income = income_form.save(commit=False)
#             income.user = request.user  # Set the user to the logged-in user
#             income.save()

#             if (
#                 income_type_form.is_valid()
#                 and income_type_form.cleaned_data.get('recurring_type')
#                 and recurring_income_form.is_valid()
#             ):
#                 recurring_income = recurring_income_form.save(commit=False)
#                 recurring_income.income = income
#                 recurring_income.save()

#             if (
#                 income_type_form.is_valid()
#                 and income_type_form.cleaned_data.get('variation_type')
#                 and varied_recurring_income_form.is_valid()
#             ):
#                 varied_recurring_income = varied_recurring_income_form.save(commit=False)
#                 varied_recurring_income.re_income = recurring_income
#                 varied_recurring_income.save()

#             return redirect('income-home')

#     else:
#         income_form = IncomeForm(instance=income)
#         recurring_income_form = RecurringIncomeForm(instance=recurring_income)
#         varied_recurring_income_form = VariedRecurringIncomeForm(instance=varied_recurring_income)
#         income_type_form = IncomeTypeForm()

#     return render(
#         request,
#         'income/add-income.html',
#         {
#             'income_form': income_form,
#             'recurring_income_form': recurring_income_form,
#             'varied_recurring_income_form': varied_recurring_income_form,
#             'income_type_form': income_type_form,
#         },
#     )


# @login_required_view
# def view_income_details(request):
#     income_details = get_all_income_details()
#     return render(request, 'income/home.html', {'income_details': income_details})


# @login_required_view
# def get_income_details(request, income_id):
#     income = Income.objects.filter(id=income_id,).first()
#     recurring_income, varied_recurring_income = get_recurring_income_details(income)

#     allincome = {
#         'income': None,
#         'recurring_income': None,
#         'varied_recurring_income': None,
#     }

#     if income:
#         allincome['income'] = {
#             'id': income.id,
#             'amount': income.amount,
#             'source': income.source,
#             'description': income.description,
#             'day_of_month': income.day_of_month,
#         }

#         if recurring_income:
#             allincome['recurring_income'] = {
#                 'recurring_type': recurring_income.recurring_type,
#                 'recurring_day': recurring_income.recurring_day,
#                 'recurring_range': recurring_income.recurring_range,
#             }

#         if varied_recurring_income:
#             allincome['varied_recurring_income'] = {
#                 'variation_type': varied_recurring_income.variation_type,
#                 'variation_amount': varied_recurring_income.variation_amount,
#                 'variation_percentage': varied_recurring_income.variation_percentage,
#                 'variation_period': varied_recurring_income.variation_period,
#                 'variation_description': varied_recurring_income.variation_description,
#             }

#     return render(request, 'income/income-detail.html', {'allincome': allincome})


# @login_required_view
# def no_data(request):
#     return HttpResponseNotFound("Record not found")
@login_required_view
def edit_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)

    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income-home')
    else:
        form = IncomeForm(instance=income)

    return render(request, 'income/edit-income.html', {'form': form, 'income': income})

@login_required_view
def deleteincome(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)

    if request.method == 'POST':
        try:
            income.delete()
            return redirect('income-home')
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

    return HttpResponseBadRequest("Invalid Request")

@login_required_view
def delete_selected_income(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')

        try:
            Income.objects.filter(id__in=selected_items, user=request.user).delete()
            return redirect('income-home')
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

    return HttpResponseBadRequest("Invalid Request")

@login_required_view
def create_income(request, income_id=None):
    income = get_object_or_404(Income, id=income_id) if income_id else None
    recurring_income = RecurringIncome.objects.filter(income=income).first() if income else None
    varied_recurring_income = (
        VariedRecurringIncome.objects.filter(re_income__income=income).first()
        if recurring_income
        else None
    )

    if request.method == 'POST':
        income_form = IncomeForm(request.POST, instance=income)
        recurring_income_form = RecurringIncomeForm(request.POST, instance=recurring_income)
        varied_recurring_income_form = VariedRecurringIncomeForm(
            request.POST, instance=varied_recurring_income
        )
        income_type_form = IncomeTypeForm(request.POST)

        if income_form.is_valid():
            income = income_form.save(commit=False)
            income.user = request.user  # Set the user to the logged-in user
            income.save()

            if (
                income_type_form.is_valid()
                and income_type_form.cleaned_data.get('recurring_type')
                and recurring_income_form.is_valid()
            ):
                recurring_income = recurring_income_form.save(commit=False)
                recurring_income.income = income
                recurring_income.save()

            if (
                income_type_form.is_valid()
                and income_type_form.cleaned_data.get('variation_type')
                and varied_recurring_income_form.is_valid()
            ):
                varied_recurring_income = varied_recurring_income_form.save(commit=False)
                varied_recurring_income.re_income = recurring_income
                varied_recurring_income.save()

            return redirect('income-home')

    else:
        income_form = IncomeForm(instance=income)
        recurring_income_form = RecurringIncomeForm(instance=recurring_income)
        varied_recurring_income_form = VariedRecurringIncomeForm(instance=varied_recurring_income)
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

@login_required_view
def view_income_details(request):
    income_details = get_all_income_details(request.user)
    return render(request, 'income/home.html', {'income_details': income_details})

@login_required_view
def get_income_details(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    recurring_income, varied_recurring_income = get_recurring_income_details(income)

    allincome = {
        'income': None,
        'recurring_income': None,
        'varied_recurring_income': None,
    }

    if income:
        allincome['income'] = {
            'id': income.id,
            'amount': income.amount,
            'source': income.source,
            'description': income.description,
            'day_of_month': income.day_of_month,
        }

        if recurring_income:
            allincome['recurring_income'] = {
                'recurring_type': recurring_income.recurring_type,
                'recurring_day': recurring_income.recurring_day,
                'recurring_range': recurring_income.recurring_range,
            }

        if varied_recurring_income:
            allincome['varied_recurring_income'] = {
                'variation_type': varied_recurring_income.variation_type,
                'variation_amount': varied_recurring_income.variation_amount,
                'variation_percentage': varied_recurring_income.variation_percentage,
                'variation_period': varied_recurring_income.variation_period,
                'variation_description': varied_recurring_income.variation_description,
            }

    return render(request, 'income/income-detail.html', {'allincome': allincome})

@login_required_view
def no_data(request):
    return HttpResponseNotFound("Record not found")