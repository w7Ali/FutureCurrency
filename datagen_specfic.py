import json
from faker import Faker
from datetime import date as datetime_date

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime_date):
            return obj.isoformat()
        return super().default(obj)

fake = Faker()

# Generate expenses data
expenses = [
    {
        "model": "expenses.expense",
        "pk": i,
        "fields": {
            "name": fake.word(),
            "amount": fake.random_int(min=100, max=10000, step=100),
            "category": fake.word(),
            "description": fake.sentence(),
            "date": fake.date_between(start_date="-30d", end_date="today"),
        },
    }
    for i in range(1, 51)
]

# Generate income data
income = [
    {
        "model": "income.income",
        "pk": i,
        "fields": {
            "amount": fake.random_int(min=1000, max=50000, step=1000),
            "source": fake.word(),
            "description": fake.sentence(),
            "day_of_month": fake.random_int(min=1, max=28),
        },
    }
    for i in range(1, 51)
]

# Generate recurring income data related to income, emi, and expenses
recurring_income = [
    {
        "model": "income.recurringincome",
        "pk": i,
        "fields": {
            "recurring_type": "M",
            "recurring_day": fake.random_int(min=1, max=28),
            "recurring_range": fake.random_int(min=1, max=12),
            "related_income": fake.random_int(min=1, max=50),
            "related_expense": fake.random_int(min=1, max=50),
            # Add other fields as needed
        },
    }
    for i in range(1, 51)
]

# Combine all data for your apps
all_data = expenses + income + recurring_income

# Dump data to initial_data.json using custom encoder
with open("initial_data2.json", "w") as json_file:
    json.dump(all_data, json_file, indent=2, cls=DateEncoder)

print("Data generation complete.")
