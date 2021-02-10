from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# from django.urls import reverse

from basketapp.models import BasketItem


@login_required
def index(request):
    basket = request.user.basket.all()
    context = {
        'page_title': 'корзина',
        'basket': basket,
    }
    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, product_pk):
    basket_item, _ = BasketItem.objects.get_or_create(
        user=request.user,
        product_id=product_pk
    )
    basket_item.qty += 1
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, basket_item_pk):
    item = get_object_or_404(BasketItem, pk=basket_item_pk)
    item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
