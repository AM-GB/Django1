from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    menu = [
        {'category': 'все', },
        {'category': 'кросовки', },
        {'category': 'форма', },
        {'category': 'мятчи', },
        {'category': 'аксессуары', },
    ]
    context = {
        'page_title': 'продукты',
        'menu': menu,
    }
    return render(request, 'mainapp/products.html', context)


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
