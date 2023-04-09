from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.decorators.http import require_http_methods, require_GET, require_POST, require_safe

# Create your views here.
@require_http_methods(['POST', 'GET'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect('movies:index')
        else:
            form = AuthenticationForm()

        context = {'form': form}
        return render(request, 'accounts/login.html', context)

@require_POST
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

@require_http_methods(['POST', 'GET'])
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect('movies:index')
        else:
            form = CustomUserCreationForm()
        context = {
            'form' : form,
        }
        return render(request, 'accounts/signup.html', context)
    else:
        return redirect('movies:index')

@require_POST
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('movies:index')

@require_http_methods(['POST', 'GET'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)

@require_http_methods(['POST', 'GET'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/change_password.html', context)