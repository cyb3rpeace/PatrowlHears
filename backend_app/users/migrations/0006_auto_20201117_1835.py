# Generated by Django 3.0.10 on 2020-11-17 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200512_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorgsettings',
            name='max_monitored_items',
            field=models.IntegerField(default=100000, null=True),
        ),
        migrations.AlterField(
            model_name='orgsettings',
            name='max_monitored_items',
            field=models.IntegerField(default=100000, null=True),
        ),
    ]
