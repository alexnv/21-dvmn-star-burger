# Generated by Django 3.2.15 on 2023-08-04 12:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_order_is_new_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='item_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена в заказе'),
        ),
    ]
