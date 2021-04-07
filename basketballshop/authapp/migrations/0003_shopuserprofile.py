# Generated by Django 2.2 on 2021-04-06 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20210404_0735'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopUserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('tagline', models.CharField(blank=True, max_length=128, verbose_name='теги')),
                ('about_me', models.TextField(blank=True, verbose_name='о себе')),
                ('gender', models.CharField(blank=True, choices=[('M', 'мужской'), ('W', 'женский')], max_length=1, verbose_name='пол')),
            ],
        ),
    ]
