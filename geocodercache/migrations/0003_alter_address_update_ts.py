# Generated by Django 3.2.15 on 2023-08-04 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geocodercache', '0002_alter_address_update_ts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='update_ts',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='изменён в'),
        ),
    ]
