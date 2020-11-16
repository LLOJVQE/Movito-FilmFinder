from django.contrib import admin

# Register your models here.

from . import models


class UsersAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ('Id', {'fields': ['id']}),
    #     ('UserName',        {'fields': ['username']}),
    #     ('Create Time', {'fields': ['c_time']}),
    # ]
    # inlines = [ChoiceInline]
    list_display = ( 'username', 'id', 'c_time')
    list_filter = ['c_time']
    search_fields = ['username']

admin.site.register(models.User,UsersAdmin)
# admin.site.register(models.Wishlist)
admin.site.register(models.Bannedlist)
admin.site.register(models.Comment)