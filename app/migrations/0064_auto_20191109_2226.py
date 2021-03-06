# Generated by Django 2.2.7 on 2019-11-09 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0063_auto_20191109_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.Status'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='<function uuid4 at 0x7f7c972679d8>', editable=False, max_length=255),
        ),
    ]
