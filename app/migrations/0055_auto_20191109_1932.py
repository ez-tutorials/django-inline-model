# Generated by Django 2.2.7 on 2019-11-09 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_auto_20191109_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.UUIDField(default='a326dd6a-39b7-4b94-b739-2c8d100da1fd'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='78f22cb6-1fa8-443b-9852-e9ffd28aa44f'),
        ),
    ]
