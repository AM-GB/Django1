from django.contrib import auth
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserCreationForm, ShopUserChangeForm


def login(request):
    redirect_to = request.GET.get('next', '')

    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            redirect_to = request.POST.get('redirect-to')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(redirect_to or reverse('base:index'))
    else:
        form = ShopUserLoginForm()

    context = {
        'page_title': 'логин',
        'form': form,
        'redirect_to': redirect_to,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('base:index'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserCreationForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = False
            user.set_activation_code()
            user.save()
            if not user.send_email_for_confirmation():
                return HttpResponseRedirect(reverse('auth:register'))
            return HttpResponseRedirect(reverse('base:index'))
    else:
        register_form = ShopUserCreationForm()

    context = {
        'page_title': 'регистрация',
        'form': register_form,
    }
    return render(request, 'authapp/register.html', context)


def edit(request):
    if request.method == 'POST':
        form = ShopUserChangeForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('base:index'))
    else:
        form = ShopUserChangeForm(instance=request.user)

    context = {
        'page_title': 'редактирование',
        'form': form,
    }
    return render(request, 'authapp/update.html', context)


def verify(request, email, activate_code):
    user = get_user_model().objects.filter(email=email).first()
    if user.activate_code == activate_code and not user.is_activation_key_expired:
        user.is_active = True
        user.save()
        auth.login(request, user)
    return render(request, 'authapp/verification.html')
