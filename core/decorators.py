from django.contrib.auth.decorators import login_required
from functools import wraps

def login_required_view(view_func):
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return wrapped_view
