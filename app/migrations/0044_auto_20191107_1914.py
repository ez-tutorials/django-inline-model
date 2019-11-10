# Generated by Django 2.2.7 on 2019-11-07 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_auto_20191107_1410'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='component',
            options={'ordering': ['-product__name']},
        ),
        migrations.AlterModelOptions(
            name='part',
            options={'get_latest_by': 'modified', 'ordering': ('-modified', '-created')},
        ),
        migrations.AddField(
            model_name='part',
            name='part_code',
            field=models.UUIDField(default='69ab3eeb-f06a-4039-9e1d-d18374912219'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='0bbbc2b7-20ff-43b3-9a83-0e3bc54d0603'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='number',
            field=models.UUIDField(default='416c9607-9b22-47d0-ae63-01cc16f1110d', unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='part',
            unique_together=set(),
        ),
    ]