# # views.py
# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse, HttpResponseBadRequest
# from core.decorators import login_required_view  # Import the custom decorator

# from .models import Emi, EmiBalance, Expense
# from .forms import EmiForm
# from .forms import ExpenseForm
# from django.contrib import messages


# @login_required_view
# def expensehome(request):
#     emis = Emi.objects.filter(user=request.user)
#     expenses = Expense.objects.filter(user=request.user)

#     # return render(request, 'expenses/emi_list.html', {'emis': emis})
#     return render(request, 'expenses/home.html', {'emis': emis,'expenses':expenses})
# #----------------------------------------------------------------------------------------------------#


# @login_required_view
# def expense_create(request):
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             expense = form.save(commit=False)
#             expense.user = request.user
#             expense.save()
#             messages.add_message(request, messages.SUCCESS, "Added Successfully")
#             return redirect('expense-home')
#     else:
#         form = ExpenseForm()
#     return render(request, 'expenses/expense_form.html', {'exform': form, 'action': 'Create'})


# @login_required_view
# def emi_create(request):
#     if request.method == 'POST':
#         form = EmiForm(request.POST)
#         if form.is_valid():
#             emi = form.save(commit=False)
#             emi.user = request.user
#             emi.save()
#             return redirect('expense-home')
#     else:
#         form = EmiForm()
#     return render(request, 'expenses/emi_form.html', {'form': form, 'action': 'Create'})



# @login_required_view
# def emi_detail(request, pk):
#     emi = get_object_or_404(Emi, pk=pk)
#     # alldetail = EmiBalance.objects.all()

#     return render(request, 'expenses/emi_detail.html', {'emi': emi})

# @login_required_view
# def emi_update(request, pk):
#     emi = get_object_or_404(Emi, pk=pk)
#     if request.method == 'POST':
#         form = EmiForm(request.POST, instance=emi)
#         if form.is_valid():
#             form.save()
#             return redirect('expense-home')
#     else:
#         form = EmiForm(instance=emi)
#     return render(request, 'expenses/emi_form.html', {'form': form, 'action': 'Update'})


# @login_required_view
# def emi_delete(request, pk):
#     emi = get_object_or_404(Emi, pk=pk)
#     emi.delete()
#     return redirect('expense-home')


# @login_required_view
# def exp_delete(request, pk):
#     exp = get_object_or_404(Expense, pk=pk)
#     exp.delete()
#     return redirect('expense-home')



# @login_required_view
# def emi_update(request, pk):
#     emi = get_object_or_404(Emi, pk=pk)
#     if request.method == 'POST':
#         form = EmiForm(request.POST, instance=emi)
#         if form.is_valid():
#             form.save()
#             return redirect('expense-home')
#     else:
#         form = EmiForm(instance=emi)
#     return render(request, 'expenses/emi_form.html', {'form': form, 'action': 'Update'})


# @login_required_view
# def exp_update(request, pk):
#     exp = get_object_or_404(Expense, pk=pk)
#     if request.method == 'POST':
#         form = EmiForm(request.POST, instance=exp)
#         if form.is_valid():
#             form.save()
#             return redirect('expense-home')
#     else:
#         form = ExpenseForm(instance=exp)
#     return render(request, 'expenses/emi_form.html', {'form': form, 'action': 'Update'})




# @login_required_view
# def delete_expenses(request):
#     if request.method == 'POST':
#         selected_items = request.POST.getlist('selected_items')

#         try:
#             Expense.objects.filter(id__in=selected_items).delete()
#             return redirect('expense-home')
#         except Exception as e:
#             return HttpResponseBadRequest(f"Error: {str(e)}")

#     return HttpResponseBadRequest("Invalid Request")



# @login_required_view
# def delete_emis(request):
#     if request.method == 'POST':
#         selected_items = request.POST.getlist('selected_items')

#         try:
#             Emi.objects.filter(id__in=selected_items).delete()
#             return redirect('expense-home')
#         except Exception as e:
#             return HttpResponseBadRequest(f"Error: {str(e)}")

#     return HttpResponseBadRequest("Invalid Request")
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from core.decorators import login_required_view  # Import the custom decorator
from .models import Emi, EmiBalance, Expense
from .forms import EmiForm, ExpenseForm
from django.contrib import messages

@login_required_view
def expensehome(request):
    emis = Emi.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    return render(request, 'expenses/home.html', {'emis': emis, 'expenses': expenses})

@login_required_view
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.add_message(request, messages.SUCCESS, "Added Successfully")
            return redirect('expense-home')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'exform': form, 'action': 'Create'})

@login_required_view
def emi_create(request):
    if request.method == 'POST':
        form = EmiForm(request.POST)
        if form.is_valid():
            emi = form.save(commit=False)
            emi.user = request.user
            emi.save()
            return redirect('expense-home')
    else:
        form = EmiForm()
    return render(request, 'expenses/emi_form.html', {'form': form, 'action': 'Create'})

@login_required_view
def emi_detail(request, pk):
    emi = get_object_or_404(Emi, pk=pk)
    return render(request, 'expenses/emi_detail.html', {'emi': emi})

@login_required_view
def emi_update(request, pk):
    emi = get_object_or_404(Emi, pk=pk)
    if request.method == 'POST':
        form = EmiForm(request.POST, instance=emi)
        if form.is_valid():
            form.save()
            return redirect('expense-home')
    else:
        form = EmiForm(instance=emi)
    return render(request, 'expenses/emi_form.html', {'form': form, 'action': 'Update'})

@login_required_view
def emi_delete(request, pk):
    emi = get_object_or_404(Emi, pk=pk)
    emi.delete()
    return redirect('expense-home')

@login_required_view
def exp_delete(request, pk):
    exp = get_object_or_404(Expense, pk=pk)
    exp.delete()
    return redirect('expense-home')

@login_required_view
def exp_update(request, pk):
    exp = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=exp)
        if form.is_valid():
            form.save()
            return redirect('expense-home')
    else:
        form = ExpenseForm(instance=exp)
    return render(request, 'expenses/expense_form.html', {'exform': form, 'action': 'Update'})

@login_required_view
def delete_expenses(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        try:
            Expense.objects.filter(id__in=selected_items).delete()
            return redirect('expense-home')
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")
    return HttpResponseBadRequest("Invalid Request")

@login_required_view
def delete_emis(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        try:
            Emi.objects.filter(id__in=selected_items).delete()
            return redirect('expense-home')
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")
    return HttpResponseBadRequest("Invalid Request")
