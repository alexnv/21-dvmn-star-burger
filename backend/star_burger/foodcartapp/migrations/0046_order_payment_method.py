# Generated by Django 3.2.15 on 2023-08-04 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0045_auto_20230804_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('NA', 'Не известно'), ('ON', 'Электронно'), ('CH', 'Наличностью')], default='NA', max_length=2),
        ),
    ]