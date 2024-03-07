from django.shortcuts import render
from core.decorators import login_required_view

@login_required_view
# Create your views here.
def home(request):
    user_details = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'date_joined': request.user.date_joined,
        'last_login': request.user.last_login,
        # Add other user attributes as needed
    }

    return render(request, 'core/dashboard.html', {'user_details': user_details})



