from mainapp.models import ProductCategory


def categories(request):
    return {
        'menu': ProductCategory.objects.filter(is_active=True)
    }
