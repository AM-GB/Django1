import random

from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache

from basketballshop import settings
from mainapp.models import ProductCategory, Product


def get_products():
    if settings.LOW_CACHE:
        key = 'all_products'
        products = cache.get(key)
        if products is None:
            products = Product.get_items()
            cache.set(key, products)
        return products
    return Product.get_items()


def get_products_by_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}_products'
        products = cache.get(key)
        if products is None:
            products = Product.get_items().filter(category_id=pk)
            cache.set(key, products)
        return products
    return Product.get_items().filter(category_id=pk)


def get_hot_product():
    product_ids = get_products(). \
        values_list('id', flat=True)
    random_id = random.choice(product_ids)
    return Product.objects.get(pk=random_id)


def same_products(hot_product):
    return Product.get_items().filter(category=hot_product.category). \
        exclude(pk=hot_product.pk)[:3]


def index(request):
    print(request.headers)
    context = {
        'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    product_1 = get_hot_product()
    description_product_1 = []

    for descript in product_1.description.split('|'):
        description_product_1.append({'description': descript, })

    context = {
        'page_title': 'продукты',
        'product_1': product_1,
        'description': description_product_1,
        'same_products': same_products(product_1),
    }

    return render(request, 'mainapp/products.html', context)


def category(request, pk):
    page_num = request.GET.get('page', 1)
    if pk == 0:
        category = {'pk': 0, 'name': 'все'}
        products = get_products()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = get_products_by_category(pk)

    products_paginator = Paginator(products, 2)
    try:
        products = products_paginator.page(page_num)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': 'товары категории',
        'category': category,
        'products': products,
    }
    return render(request, 'mainapp/category_products.html', context)


def product_page(request, pk):
    description_product_1 = []
    for descript in get_hot_product().description.split('|'):
        description_product_1.append({'description': descript, })

    product = get_object_or_404(Product, pk=pk)
    context = {
        'page_title': 'страница продукта',
        'product': product,
        'description': description_product_1,
    }
    return render(request, 'mainapp/product_page.html', context)


def contact(request):
    contacts = [
        {'city': 'Краснодар',
         'phone': '+7-918-123-1234',
         'email': 'infoK@basketballshop',
         'address': 'Казань арена', },
        {'city': 'Казань',
         'phone': '+7-918-123-1235',
         'email': 'infoKz@basketballshop',
         'address': 'Парк Галицкого', },
        {'city': 'Санкт-петербург',
         'phone': '+7-918-123-1233',
         'email': 'infoS@basketballshop',
         'address': 'Эрмитаж', },
    ]
    context = {
        'page_title': 'контакты',
        'contacts': contacts,
    }
    return render(request, 'mainapp/contact.html', context)


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=pk).first()
        return JsonResponse(
            {'price': product and product.price or 0}
        )


def db_profile_by_type(sender, q_type, queries):
    print(f'db profile {q_type} for {sender}:')
    for query in filter(lambda x: q_type in x,
                        map(lambda x: x['sql'],
                            queries)):
        print(query)


@receiver(pre_save, sender=ProductCategory)
def update_prod_cat_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
