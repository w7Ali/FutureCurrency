# import os
# import sys
# import csv
# from pathlib import Path
# from datetime import datetime
#
# BASE_DIR = Path(__file__).resolve().parent.parent
#
# # Add the project directory to the sys.path
# sys.path.append(BASE_DIR.parent.parent)
#
# # Set the Django settings module to your project's settings module
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
# import django
# django.setup()
#
# from expenses.models import Expense, Emi, EmiBalance
#
# # Function to convert string date to datetime object
# def parse_date(date_str):
#     return datetime.strptime(date_str, '%Y-%m-%d')
#
# # Import Expenses from CSV and save to models
# with open('data/expense.csv', 'r') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         Expense.objects.create(
#             amount=row['amount'],
#             category=row['category'],
#             description=row['description'],
#             date=parse_date(row['date'])
#         )
#
# # Import Emis from CSV and save to models
# with open('emis.csv', 'r') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         Emi.objects.create(
#             product_name=row['product_name'],
#             down_payment=row['down_payment'],
#             emi_amount=row['emi_amount'],
#             start_date=parse_date(row['start_date']),
#             due_date=row['due_date'],
#             emi_count=row['emi_count'],
#             interest_percent=row['interest_percent']
#         )
#
# # Import EmiBalances from CSV and save to models
# with open('emi_balances.csv', 'r') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         emi_instance = Emi.objects.get(product_name=row['product_name'])
#         EmiBalance.objects.create(
#             emi=emi_instance,
#             paid_amount=row['paid_amount'],
#             remaining_emis=row['remaining_emis'],
#             pending_amount=row['pending_amount'],
#             total_amount=row['total_amount']
#         )
#
# print("Data import completed successfully.")
