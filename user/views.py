from django.shortcuts import render, redirect
from .forms import SignupFrom, UserChangeCustom, AdminChangeCustom
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from core.decorators import login_required_view
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


# Singup
def user_signup(request):
    if request.method == 'POST':
        fm = SignupFrom(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Registration Successful")
            return redirect('login')
        else:
            messages.error(request, "Account Not Created. Please check the form for errors.")
            print(fm.errors)

    else:
        fm = SignupFrom()

    return render(request, 'user/signup.html', {'fm': fm})

# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Login Successful")
                    return redirect('welcome-home')
                else:
                    messages.error(request, "Invalid username or password.")
        else:
            fm = AuthenticationForm()
        return render(request, 'user/login.html', {'fm': fm})
    else:
        return redirect('welcome-home')

# LogOut
def user_logout(request):
    logout(request)
    return redirect('index_page')


# Rest Password
@login_required_view
def user_reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed successfully.')
            update_session_auth_hash(request, form.user) #it will prevent user to forcefully logout
            return redirect('welcome-home')  # Assuming 'home' is the name of your home page URL
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'user/change-password.html', {'form': form})

@login_required_view
def user_edit_profile(request):
    user_instance = request.user
    all_user = None

    form_class = AdminChangeCustom if request.user.is_superuser else UserChangeCustom

    if request.method == 'POST':
        fm = form_class(request.POST, instance=user_instance)
        if fm.is_valid():
            fm.save()
            return redirect('welcome-home')
    else:
        fm = form_class(instance=user_instance)

    if request.user.is_superuser:
        all_user = User.objects.all()

    return render(request, 'user/edit-user.html', context={'form': fm, 'all_user': all_user})


@login_required_view
def user_details(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Permission Denied: You do not have the required permissions.")

    # form_class = AdminChangeCustom
    user_one = User.objects.get(id=id)

    if request.method == 'POST':
        userfm = UserChangeCustom(request.POST, instance=user_one)
        if userfm.is_valid():
            userfm.save()
            print("Form saved successfully.")
            return redirect('edit-profile')
        else:
            print("Form is not valid. Errors:", userfm.errors)
    else:
        userfm = UserChangeCustom(instance=user_one)

    return render(request, 'user/user-details.html', context={'detailuser': user_one ,'user': userfm})
