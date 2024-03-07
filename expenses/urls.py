# urls.py
from django.urls import path
from .views import expensehome, emi_detail, emi_create, emi_update, emi_delete, expense_create,delete_expenses, delete_emis

urlpatterns = [
    path('emi/', expensehome, name='expense-home'),
    path('emi/<int:pk>/', emi_detail, name='emi_detail'),
    path('emi/create/', emi_create, name='emi_create'),
    path('expense/create/', expense_create, name='expense_create'),
    path('emi/update/<int:pk>/', emi_update, name='emi_update'),
    path('emi/delete/<int:pk>/', emi_delete, name='emi_delete'),
    path('delete_expenses/', delete_expenses, name='delete_expenses'),
    path('delete_emis/', delete_emis, name='delete_emis'),
]
