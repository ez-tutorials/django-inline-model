# Generated by Django 2.2.7 on 2019-11-04 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20191104_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='component_part', to='app.Part'),
        ),
        migrations.AlterField(
            model_name='component',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='component_warehouse', to='app.Warehouse'),
        ),
    ]