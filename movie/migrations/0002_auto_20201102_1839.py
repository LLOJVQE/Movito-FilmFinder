# Generated by Django 3.1.2 on 2020-11-02 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False, verbose_name='director_id')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'director',
                'verbose_name_plural': 'director',
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='director_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='movie.director', verbose_name='Director'),
        ),
    ]
