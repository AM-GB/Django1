import hashlib
import random
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.timezone import now

from basketballshop.settings import DOMAIN_NAME, EMAIL_HOST_USER, ACTIVATION_KEY_TTL


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField('возраст', null=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    activate_code = models.CharField(max_length=128, blank=True)
    registration_start_time = models.DateTimeField(
        auto_now_add=True, null=True)

    @cached_property
    def basket_items(self):
        # return self.basket.all()
        return self.basket.select_related('product').all()

    def basket_price(self):
        return sum(el.product_cost for el in self.basket_items)

    def basket_qty(self):
        return sum(el.qty for el in self.basket_items)

    @property
    def is_activation_key_expired(self):
        return now() - self.registration_start_time > timedelta(hours=ACTIVATION_KEY_TTL)

    def set_activation_code(self):
        salt = hashlib.sha1(
            str(random.random()).encode('utf8')).hexdigest()[:6]
        self.activate_code = hashlib.sha1(
            (self.email + salt).encode('utf8')).hexdigest()

    def send_email_for_confirmation(self):
        verify_link = reverse('auth:verify',
                              kwargs={'email': self.email,
                                      'activate_code': self.activate_code})

        subject = f'Подтверждение учетной записи {self.username}'
        message = f'Для подтверждения учетной записи {self.username} на портале ' \
                  f'{DOMAIN_NAME} перейдите по ссылке: \n{DOMAIN_NAME}{verify_link}'

        return send_mail(subject, message, EMAIL_HOST_USER, [self.email],
                         fail_silently=False)


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'мужской'),
        (FEMALE, 'женский'),
    )

    user = models.OneToOneField(
        ShopUser, primary_key=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='о себе', blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1,
                              choices=GENDER_CHOICES, blank=True)
