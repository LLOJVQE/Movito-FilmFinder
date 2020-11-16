# coding=utf-8

"""
Author: Yao Zhao
Create Date: 2020-10-13
@Software: Pycharm
"""

from django.urls import path
from django.conf.urls import url
from .views import UserInfoView, WishListView,BannedListView, OthersUserInfoView,OthersWishListView
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url,include
from login import views
import movie

urlpatterns = [
    # path('', movie.views.IndexView.as_view(), name='index'),
    # path('movie/',include('movie.urls')),
    # path('movie/',views.IndexView.as_view(), name='index'),


    path('l/', views.Login, name='login'),
    # 验证码
    # path('get_auth_img/', views.GetAuthImg.as_view(), name="get_auth_img"),
    path('login_index/', views.index, name='index'),

    path('register/', views.Register, name='register'),
    # path('logout/', views.Logout, name='logout'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # 用户信息
    url(r'^profile/$', UserInfoView.as_view(), name="user_account"),
    url(r'^wishlist/(?P<username>.*)/$', WishListView.as_view(), name="wishlist"),
    url(r'^bannedlist/$', BannedListView.as_view(), name="bannedlist"),
    url(r'^del_wishlist/(?P<movie_id>.*)/$', views.Del_wishlist.as_view(), name='del_wishlist'),
    url(r'^others_profile/(?P<username>.*)/$', OthersUserInfoView.as_view(), name="other_user_account"),
    url(r'^others_wishlist/(?P<username>.*)/$', OthersWishListView.as_view(), name="others_wishlist"),
    url(r'^add_bannedlist/(?P<username>.*)/$', views.AddBannedView.as_view(), name='add_bannedlist'),
    url(r'^del_bannedlist/(?P<username>.*)/$', views.DelBannedView.as_view(), name='del_bannedlist'),
    # path('profile/', views.ModifyInfo, name='modify_info'),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)