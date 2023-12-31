# Generated by Django 3.2.15 on 2023-08-04 12:56

from django.db import migrations

from django.db import models


def update_total(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    for oi in OrderItem.objects.all():
        oi.item_price = oi.product.price
        oi.save()


def update_total_order(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    order_items = OrderItem.objects.all().annotate(
        calculated_price=models.Sum(
            models.F('product__price') * models.F('quantity')
        ))
    for oi in order_items:
        oi.total = oi.calculated_price
        oi.save()


class Migration(migrations.Migration):
    dependencies = [
        ('foodcartapp', '0041_orderitem_item_price'),
    ]

    operations = [
        migrations.RunPython(update_total),
        migrations.RunPython(update_total_order),
    ]
