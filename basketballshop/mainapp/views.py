from django.shortcuts import render, get_object_or_404

from mainapp.models import ProductCategory, Product


def get_menu():
    return ProductCategory.objects.all()


def index(request):
    context = {
        'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    # menu = ProductCategory.objects.all()
    # menu = [{'category': 'все', }]

    # for item in category:
    #     menu.append({'category': item.name})

    # menu = [
    #     {'category': 'все', },
    #     {'category': 'кросовки', },
    #     {'category': 'форма', },
    #     {'category': 'мятчи', },
    #     {'category': 'аксессуары', },
    # ]

    product_1 = Product.objects.all()[0]
    description_product_1 = []

    for descript in product_1.description.split('|'):
        description_product_1.append({'description': descript, })

    context = {
        'page_title': 'продукты',
        'menu': get_menu(),
        'product_1': product_1,
        'description': description_product_1,
    }

    return render(request, 'mainapp/products.html', context)


def category(request, pk):
    if pk == 0:
        category = {'pk': 0, 'name': 'все'}
        products = Product.objects.all()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = category.product_set.all()

    context = {
        'page_title': 'товары категории',
        'menu': get_menu(),
        'category': category,
        'products': products,
    }
    return render(request, 'mainapp/category_products.html', context)


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
        {'city': 'Свнкт-петербург',
         'phone': '+7-918-123-1233',
         'email': 'infoS@basketballshop',
         'address': 'Эрмитаж', },
    ]
    context = {
        'page_title': 'контакты',
        'contacts': contacts,
    }
    return render(request, 'mainapp/contact.html', context)
