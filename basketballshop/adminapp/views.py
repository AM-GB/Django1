from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import AdminShopUserUpdateForm
from mainapp.models import ProductCategory


@user_passes_test(lambda user: user.is_superuser)
def index(request):
    all_users = get_user_model().objects.all()
    context = {
        'page_title': 'админка/пользователи',
        'all_users': all_users,
    }
    return render(request, 'adminapp/index.html', context)


@user_passes_test(lambda user: user.is_superuser)
def user_update(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.method == 'POST':
        user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('new_admin:index'))
    else:
        user_form = AdminShopUserUpdateForm(instance=user)

    context = {
        'page_title': 'админка/пользователи/редактирование',
        'form': user_form
    }
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda user: user.is_superuser)
def user_delete(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    # user.delete()
    if not user.is_active or request.method == 'POST':
        if user.is_active:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return HttpResponseRedirect(reverse('new_admin:index'))
    context = {
        'page_title': 'админка/пользователи/удаление',
        'user_to_delete': user
    }
    return render(request, 'adminapp/user_delete.html', context=context)


@user_passes_test(lambda user: user.is_superuser)
def categories(request):
    context = {
        'page_title': 'админка/категории',
        'category_list': ProductCategory.objects.all()
    }
    return render(request, 'adminapp/categories.html', context=context)
