from django.db import models
from movie.models import Movie
from datetime import datetime

# Create your models here.
# login/models.py

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''User Info'''
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=128, unique=True, verbose_name='User Name')
    info = models.TextField(verbose_name="Personal profile", default='Hi!')
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
    password = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')
    wishlist = models.ManyToManyField(Movie)
    # is_authenticated=True
    # is_anonymous=False
    is_active=True
    # is_staff=True
    # has_module_perms=True
    def __str__(self):
        return self.username

    class Meta:
        ordering = ['id']
        unique_together = (("username", "email"),)
        verbose_name = 'Users'
        verbose_name_plural = 'Users'

# class Wishlist(models.Model):
#
#     user = models.ForeignKey(User, default='', on_delete=models.CASCADE, verbose_name='用户')
#     movie = models.ManyToManyField(Movie)
#     add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
#
#     class Meta:
#         ordering = ['user']
#         verbose_name = 'User\'s Wishlist'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.user.username

class Bannedlist(models.Model):
    '''Banned list'''
    user = models.ForeignKey(User, default='', on_delete=models.CASCADE, verbose_name='用户')
    banned_user = models.ManyToManyField(User,related_name='banned_user')

    class Meta:
        ordering = ['user']
        verbose_name = 'User\'s Bannedlist'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    star = models.FloatField(verbose_name='star', default=0)
    content = models.TextField(verbose_name="review content", default='')
    movie = models.ForeignKey(Movie, default='', on_delete=models.CASCADE, verbose_name='movie')
    user = models.ForeignKey(User, default='',  on_delete=models.CASCADE, verbose_name='user')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')


    class Meta:
        ordering = ['user']
        verbose_name = 'Comment'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.user.username


