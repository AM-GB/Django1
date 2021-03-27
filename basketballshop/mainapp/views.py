import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from mainapp.models import ProductCategory, Product


def get_menu():
    menu = []
    for item in ProductCategory.objects.all():
        if item.is_active == True:
            menu.append(item)
    return menu


def get_hot_product():
    product_ids = Product.objects.values_list('id', flat=True).all()
    random_id = random.choice(product_ids)
    return Product.objects.get(pk=random_id)


def same_products(hot_product):
    return Product.objects.filter(category=hot_product.category). \
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
        'menu': get_menu(),
        'product_1': product_1,
        'description': description_product_1,
        'same_products': same_products(product_1),
    }

    return render(request, 'mainapp/products.html', context)


def category(request, pk):
    page_num = request.GET.get('page', 1)
    if pk == 0:
        category = {'pk': 0, 'name': 'все'}
        products = Product.objects.all()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = category.product_set.all()

    products_paginator = Paginator(products, 2)
    try:
        products = products_paginator.page(page_num)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': 'товары категории',
        'menu': get_menu(),
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
        'menu': get_menu(),
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
