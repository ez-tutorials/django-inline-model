# Generated by Django 2.2.7 on 2019-11-06 11:27

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20191106_1126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='product_status',
            new_name='status',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=smart_selects.db_fields.GroupedForeignKey(group_field='status', on_delete=django.db.models.deletion.CASCADE, to='app.Product'),
        ),
    ]
