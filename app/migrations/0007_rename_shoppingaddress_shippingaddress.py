# Generated by Django 4.2.7 on 2023-11-20 02:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_product_detail'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShoppingAddress',
            new_name='ShippingAddress',
        ),
    ]
