# Generated by Django 3.1.2 on 2020-11-02 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genre',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False, verbose_name='IMDBID')),
                ('title', models.CharField(default='', max_length=200, verbose_name='Title')),
                ('director', models.TextField(blank=True, default='', null=True, verbose_name='导演')),
                ('genres_text', models.TextField(blank=True, default='', null=True, verbose_name='genres in text')),
                ('info', models.TextField(blank=True, default='', null=True, verbose_name='电影简介')),
                ('year', models.CharField(blank=True, max_length=10, null=True, verbose_name='Year')),
                ('run_time', models.CharField(blank=True, max_length=10, null=True, verbose_name='Run Time')),
                ('logo', models.ImageField(blank=True, default='image/default.png', null=True, upload_to='banner/%Y/%m', verbose_name='封面')),
                ('star', models.IntegerField(default=0, verbose_name='星级')),
                ('comment_nums', models.IntegerField(default=0, verbose_name='评论数')),
                ('img_path', models.TextField(blank=True, default='', verbose_name='image path')),
                ('genres', models.ManyToManyField(to='movie.Tag')),
            ],
            options={
                'verbose_name': 'Movie',
                'verbose_name_plural': 'Movie',
            },
        ),
    ]