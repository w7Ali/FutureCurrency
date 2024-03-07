from django.urls import path
from .views import AccountHome ,AddAccountView, AccountDetailView

urlpatterns = [
    path('', AccountHome.as_view(), name = 'account-home'),
    path('detail/<int:pk>/',AccountDetailView.as_view(), name = 'account-detail'),
    path('add/',AddAccountView.as_view(), name = 'add-account'),
]
