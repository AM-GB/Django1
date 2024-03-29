from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import BasketItem
from basketballshop.settings import LOGIN_URL


@login_required  # проверка аунтификации, если нет то забрасывает LOGIN_URL
def index(request):
    basket = request.user.basket.all()
    context = {
        'page_title': 'корзина',
        'basket': basket,
    }
    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, product_pk):
    if LOGIN_URL in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(
            reverse('base:product_page',
                    kwargs={'pk': product_pk}))

    basket_item, _ = BasketItem.objects.get_or_create(
        user=request.user,
        product_id=product_pk
    )
    basket_item.qty = F('qty') + 1
    basket_item.save()
    print(connection.queries)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, basket_item_pk):
    item = get_object_or_404(BasketItem, pk=basket_item_pk)
    item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update(request, basket_item_pk, qty):
    if request.is_ajax():
        item = BasketItem.objects.filter(pk=basket_item_pk).first()
        if not item:
            return JsonResponse({'status': False})
        if qty == 0:
            item.delete()
        else:
            item.qty = qty
            item.save()
        basket_summary_html = render_to_string(
            'basketapp/includes/basket_summary.html',
            request=request
        )
        print(basket_summary_html)
        return JsonResponse({'status': True,
                             'basket_summary': basket_summary_html,
                             'qty': qty})
