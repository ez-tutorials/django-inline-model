# Generated by Django 2.2.7 on 2019-11-09 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0061_auto_20191109_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='number',
            field=models.CharField(default=None, editable=False, max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='<function uuid4 at 0x7fedeb8aa9d8>', editable=False, max_length=255),
        ),
        migrations.AlterField(
            model_name='part',
            name='part_code',
            field=models.CharField(default=None, editable=False, max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(default='<function uuid4 at 0x7fedeb8aa9d8>', editable=False, max_length=255),
        ),
    ]
