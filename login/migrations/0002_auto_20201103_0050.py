# Generated by Django 3.1.2 on 2020-11-02 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_auto_20201102_2156'),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wishlist',
            field=models.ManyToManyField(to='movie.Movie'),
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
