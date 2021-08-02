from django.test import TestCase
from mainapp.models import Product, ProductCategory


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="напульсники")
        self.product_1 = Product.objects.create(name="напульсник 1",
                                                category=category,
                                                price=999.5,
                                                quantity=150)
        self.product_2 = Product.objects.create(name="напульсник 2",
                                                category=category,
                                                price=98.1,
                                                quantity=125,
                                                is_active=False)
        self.product_3 = Product.objects.create(name="напульсник 3",
                                                category=category,
                                                price=598.1,
                                                quantity=115)

    def test_product_get(self):
        product_1 = Product.objects.get(name="напульсник 1")
        product_2 = Product.objects.get(name="напульсник 2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="напульсник 1")
        product_2 = Product.objects.get(name="напульсник 2")
        self.assertEqual(str(product_1), 'напульсник 1 (напульсники)')
        self.assertEqual(str(product_2), 'напульсник 2 (напульсники)')

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="напульсник 1")
        product_3 = Product.objects.get(name="напульсник 3")
        products = product_1.get_items()
        self.assertEqual(list(products), [product_1, product_3])
