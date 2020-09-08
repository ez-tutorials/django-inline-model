# Generated by Django 2.2.7 on 2019-11-06 20:05

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20191106_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.Client'),
        ),
        migrations.AlterField(
            model_name='ordereditem',
            name='product',
            field=smart_selects.db_fields.GroupedForeignKey(group_field='order', on_delete=django.db.models.deletion.CASCADE, to='app.Product'),
        ),
    ]
