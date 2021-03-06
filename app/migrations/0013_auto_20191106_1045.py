# Generated by Django 2.2.7 on 2019-11-06 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20191106_1033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='part',
            old_name='total',
            new_name='available_total',
        ),
        migrations.AddField(
            model_name='warehouse',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='batch',
            name='supplier',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='app.Supplier'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='part',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Batch'),
        ),
        migrations.AlterField(
            model_name='part',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Warehouse'),
        ),
    ]
