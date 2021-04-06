from mainapp.models import ProductCategory


def categories(request):
    menu = []
    for item in ProductCategory.objects.all():
        if item.is_active == True:
            menu.append(item)
    return {
        'menu': menu
    }
