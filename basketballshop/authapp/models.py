from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField('возраст', null=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)

    def basket_price(self):
        return sum(el.product_cost for el in self.basket.all())

    def basket_qty(self):
        return sum(el.qty for el in self.basket.all())
