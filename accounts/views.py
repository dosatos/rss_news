from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from accounts.forms import RegistrationForm, CustomUserLoginForm
from accounts.models import CustomUser


def login_view(request):
    template = 'accounts/login.html'
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/')
        context = {'form': form, 'message': 'User or password is incorrect.'}
        return render(request, template, context)
    if request.user.is_authenticated:
        return redirect('/')
    form = CustomUserLoginForm()
    return render(request, template, {'form': form})


def register(request):
    template = 'accounts/register.html'
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, template, {'form': form})
    form = RegistrationForm()
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, template, {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def profile(request):
    template = 'accounts/profile.html'
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(request.path)
    form = PasswordChangeForm(user=request.user)
    context = {'form': form}
    return render(request, template, context)


def authenticate_user(username, password):
    try:
        user = CustomUser.objects.get(username=username)
        print(user, type(user))
        print(user, user.is_active)
        if user.check_password(password):
            return user
        else:
            return None
    except CustomUser.DoesNotExist:
        print("Such user not found")
        return None
