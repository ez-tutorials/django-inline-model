# Generated by Django 2.2.7 on 2019-11-05 12:46

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20191104_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='part',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='warehouse', chained_model_field='warehouse', on_delete=django.db.models.deletion.CASCADE, show_all=True, to='app.Part'),
        ),
        migrations.AlterField(
            model_name='component',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='component',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse', to='app.Warehouse'),
        ),
    ]
