from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from mainapp.models import Product, ProductCategory


class TestMainappSmoke(TestCase):
    fixtures = ['mainapp.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('base:products'))
        self.assertEqual(response.status_code, 200)

    def test_product_category_urls(self):
        response = self.client.get(
            reverse('base:category',
                    kwargs={'pk': 0})
        )
        self.assertEqual(response.status_code, 200)
        for category in ProductCategory.objects.all():
            response = self.client.get(
                reverse('base:category',
                        kwargs={'pk': category.pk})
            )
            self.assertEqual(response.status_code, 200)

    def test_product_urls(self):
        for product in Product.objects.all():
            response = self.client.get(f'/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)
