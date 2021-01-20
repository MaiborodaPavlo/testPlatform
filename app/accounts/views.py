from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm
from .utils import login_excluded

User = get_user_model()


@login_excluded('accounts:profile')
def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        login(request, user)
        return redirect('accounts:profile')
    return render(request, 'accounts/login.html', {'form': form})


@login_excluded('accounts:profile')
def signup_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'User created successfully.')
        return redirect('accounts:login')
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {})


class UserUpdate(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/update.html'
