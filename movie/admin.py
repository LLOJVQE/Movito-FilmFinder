from django.contrib import admin

# Register your models here.
from . import models





class MovieAdmin(admin.ModelAdmin):

    list_display = ('id','title','director', 'year')
    list_filter = ['genres','director']
    search_fields = ['title']


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(models.Movie, MovieAdmin)
admin.site.register(models.Tag, TagAdmin)