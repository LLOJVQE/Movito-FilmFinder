# Generated by Django 3.1.2 on 2020-11-11 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0007_auto_20201109_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='star_personal',
            field=models.FloatField(default=0, verbose_name='Rate_from_whitelist'),
        ),
    ]