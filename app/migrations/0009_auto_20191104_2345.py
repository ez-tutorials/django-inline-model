# Generated by Django 2.2.7 on 2019-11-04 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_component_warehouse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='component_warehouse', to='app.Part'),
        ),
    ]