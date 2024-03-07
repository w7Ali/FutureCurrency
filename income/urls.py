# income/urls.py
from django.urls import path
from .views import (
    no_data,
    deleteincome,
    delete_selected_income,
    create_income,
    view_income_details,
    get_income_details,
)


urlpatterns = [
    path('', view_income_details, name='income-home'),
    path('add-all/', create_income, name='add-all'),
    path('add-all/<int:income_id>', create_income, name='add-all'),
    path('delete/<int:income_id>/', deleteincome, name='delete-income'),
    path('mass-action/', delete_selected_income, name='mass-action'),
    path('get-income-details/<int:income_id>/', get_income_details, name='get-income-details'),
    path('get-income-details/', no_data, name='get-income-details'),

]
