# Generated by Django 2.2.7 on 2019-11-07 09:03

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20191107_0815'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='warehouse',
            new_name='packaging_warehouse',
        ),
        migrations.AlterField(
            model_name='ordereditem',
            name='product',
            field=smart_selects.db_fields.GroupedForeignKey(group_field='packaging_warehouse', on_delete=django.db.models.deletion.CASCADE, to='app.Product'),
        ),
    ]
