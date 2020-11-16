# coding=utf-8

"""
Author: Yao Zhao
Create Date: 2020-10-13
@Software: Pycharm
"""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url,include
from movie import views

urlpatterns = [

    path('', views.IndexView, name='index'),
    url(r'^search/(?P<keywords>.*)/$', views.SearchView.as_view(), name='search'),
    url(r'^searchByGenresOrDirector/(?P<keywords>.*)/$', views.SearchByGenresView.as_view(), name='search_gd'),
    url(r'^detail/(?P<movie_id>.*)-(?P<genre_id>\d+)/$', views.MovieDetailView.as_view(), name="detail"),
    url(r'^add_wishlist/(?P<movie_id>.*)/$', views.Add_wishlist.as_view(), name='add_wishlist'),
    url(r'^comment/$', views.CommentView.as_view(), name='comment'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

