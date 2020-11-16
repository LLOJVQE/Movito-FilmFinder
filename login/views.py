from __future__ import unicode_literals
from django.views.generic.base import View
from django.db import models
from login.models import User, Bannedlist, Comment
from login.forms.login import formAuth
from django import views
from pure_pagination import Paginator, PageNotAnInteger
from django.db.models import Q
from datetime import datetime,timedelta
from django.shortcuts import (
    render, redirect, reverse, HttpResponse, HttpResponseRedirect
)
from login.utils import authcode
from django.contrib.auth import authenticate, login, logout
from movie.models import Movie
import datetime
# from .forms import RegisterForm, LoginForm, UserInfoForm, ModifyPwdForm, CommentForm
import pandas as pd
import re
from django import forms
import os
import django
from django.contrib.auth.mixins import LoginRequiredMixin
# class CustomBackend(ModelBackend):
#     """
#     实现用户名邮箱均可登录
#     继承ModelBackend类，因为它有方法authenticate，可点进源码查看
#     """
#
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
#             user = User.objects.get(
#                 Q(username=username) | Q(email=username))
#             # django的后台中密码加密：所以不能password==password
#             # UserProfile继承的AbstractUser中有def check_password(self,
#             # raw_password):
#             if user.check_password(password):
#                 return user
#         except Exception as e:
#             return None

# 用户登录视图类
def Login(request):
    if request.user.is_authenticated:
        # return HttpResponse('dd')
        return HttpResponseRedirect('/movie/')
    if request.method == 'GET':
        return render(request,'login/login.html')
    if request.method == 'POST':
        username = request.POST['username']  # can be email or username
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                ###
                # request.session['user'] = username
                # return render(request,'movie/index.html')
                response = HttpResponseRedirect('/movie/')
                response.set_cookie('username', username, expires=datetime.datetime.now() + timedelta(days=1))
                response.set_cookie('url',request.get_full_path())

                # generate star_personal
                all_movie = Movie.objects.all()
                for m in all_movie:
                    movie_id = m.id

                    try:
                        bannedlist = Bannedlist.objects.get(user=user).banned_user.all()
                    except:
                        bannedlist = ''
                    comment = Comment.objects.filter(Q(movie=movie_id) & ~Q(user__in=bannedlist))
                    if comment:
                        star = sum([c.star for c in comment]) / len([c.star for c in comment])
                        # mm = Movie.objects.get(id=movie_id)
                        m.star_personal = round(star, 1)
                        m.save()


                    else:
                        # mm = Movie.objects.get(id=movie_id)
                        m.star_personal = 0
                        m.save()


                return response
            else:
                return render(request,'login/login.html',{'error_msg':'Wrong Password'})
        # elif User.objects.filter(email=username).exists():
        #
        #     user = CustomBackend().authenticate(request, username=username, password=password)
        #     if user is not None:
        #         user.backend = 'django.contrib.auth.backends.ModelBackend'
        #         login(request, user)
        #         ###
        #         user_name = user.username
        #         # request.session['user'] = user_name
        #         # return render(request,'movie/index.html')
        #         response = HttpResponseRedirect('/login/login_index/')
        #         response.set_cookie('username', user_name, expires=datetime.datetime.now() + timedelta(days=1))
        #         response.set_cookie('url', request.get_full_path())
        #
        #         return response
        #     else:
        #         return render(request, 'login/login.html', {'error_msg': 'Wrong Password'})
        else:
            return render(request, 'login/login.html', {'error_msg': 'User does not exist'})

def index(request):
    user = request.session.get('user',False)

    # return render(request,'movie/index.html',{'user':user})
    return HttpResponseRedirect('/movie/')





class UserInfoView(LoginRequiredMixin, View):
    """
    个人中心
    """
    def get(self, request):
        userID = request.COOKIES['username']
        userInfo = User.objects.get(username=userID)
        userEmail = userInfo.email
        userText = userInfo.info
        content = {
            'title': 'My Profile',
            'username': userID,
            'email': userEmail,
            'Info': userText,
        }
        return render(request, "login/profile.html",content)
    def post(self,request):
        infoform = InfoForm(request.POST)
        if infoform.is_valid():
            info = infoform.cleaned_data['info']
            username = request.user
            user = User.objects.get(username=username)
            # load block_words
            module_dir = os.path.dirname(__file__)
            file_path = os.path.join(module_dir, 'block-words.txt')  # full path to text.
            block_words = pd.read_csv(file_path,header=None)
            for word in block_words[0]:
                if info.find(word) != -1:
                    info = info.replace(word, '*' * len(word))
            user.info = info
            user.save()
            response = HttpResponseRedirect('/login/profile/')
            return response
        else:
            return HttpResponseRedirect('/login/profile/')

class OthersUserInfoView(LoginRequiredMixin, View):
    """
    个人中心
    """

    def get(self, request, username):
        userID = request.COOKIES['username']
        user = User.objects.get(username=userID)
        try:
            bannedlist = Bannedlist.objects.get(user=user).banned_user.all()
        except:
            bannedlist = ''

        userInfo = User.objects.get(username=username)
        userEmail = userInfo.email
        userText = userInfo.info
        if bannedlist == '':
            if_banned = False
        else:
            if_banned = userInfo in bannedlist
        content = {
            'title': 'My Profile',
            'username': username,
            'email': userEmail,
            'Info': userText,
            'if_banned':if_banned,
        }
        return render(request, "login/others_profile.html", content)

class WishListView(LoginRequiredMixin, View):
    """
    愿望单
    """
    def get(self, request, username):
        username = request.user
        wishlist_id = User.objects.get(username=username).wishlist.all()
        counts = wishlist_id.count()
        wishlist = Movie.objects.filter(Q(id__in= wishlist_id))
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(wishlist, 8, request=request)
        wishlist = p.page(page)

        # movies = Movie.objects.filter(Q(id__in= wishlist_id))
        # star_dic = dict()
        # for m in movies:
        #     movie_id = m.id
        #     movie = Movie.objects.get(id=movie_id)
        #     username = request.user
        #     user = User.objects.get(username=username)
        #     try:
        #         bannedlist = Bannedlist.objects.get(user=user).banned_user.all()
        #     except:
        #         bannedlist = ''
        #     comments = Comment.objects.filter(Q(movie=movie_id) & ~Q(user__in=bannedlist))
        #     if comments:
        #         star = sum([c.star for c in comments]) / len([c.star for c in comments])
        #         star_dic[movie_id] = round(star, 1)
        #     else:
        #         star_dic[movie_id] = 0

        return render(request, 'login/wishlist.html', {"wishlist": wishlist, "counts": counts})

class OthersWishListView(LoginRequiredMixin, View):
    """
    Others Wishlist
    """
    def get(self, request, username):

        wishlist_id = User.objects.get(username=username).wishlist.all()
        counts = wishlist_id.count()
        wishlist = Movie.objects.filter(Q(id__in= wishlist_id))
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(wishlist, 8, request=request)
        wishlist = p.page(page)

        # movies = Movie.objects.filter(Q(id__in= wishlist_id))
        # star_dic = dict()
        # for m in movies:
        #     movie_id = m.id
        #     movie = Movie.objects.get(id=movie_id)
        #     username = request.user
        #     user = User.objects.get(username=username)
        #     try:
        #         bannedlist = Bannedlist.objects.get(user=user).banned_user.all()
        #     except:
        #         bannedlist = ''
        #     comments = Comment.objects.filter(Q(movie=movie_id) & ~Q(user__in=bannedlist))
        #     if comments:
        #         star = sum([c.star for c in comments]) / len([c.star for c in comments])
        #         star_dic[movie_id] = round(star, 1)
        #     else:
        #         star_dic[movie_id] = 0

        return render(request, 'login/others_wishlist.html', {"wishlist": wishlist, "counts": counts})



class Del_wishlist(LoginRequiredMixin, View):
    def get(self, request, movie_id):
        username = request.COOKIES['username']
        user = User.objects.get(username=username)
        movie = Movie.objects.get(id=movie_id)
        user.wishlist.remove(movie)
        user.save()


        # return HttpResponseRedirect('/login/wishlist/')
        return HttpResponseRedirect(reverse("wishlist", args=(user.username,)))


class AddBannedView(LoginRequiredMixin, View):
    """
    add user to bannedlist
    """
    def get(self, request, username):
        user_name = request.COOKIES['username']
        user = User.objects.get(username=user_name)
        ban_user = User.objects.get(username=username)
        try:
            bannedlist = Bannedlist.objects.get(user=user)
        except:
            bannedlist = Bannedlist.objects.create(user=user)
        bannedlist.banned_user.add(ban_user)
        bannedlist.save()

        # update star_personal
        all_movie = Movie.objects.all()
        for m in all_movie:
            movie_id = m.id

            try:
                bannedlist = Bannedlist.objects.get(user=user).banned_user.all()
            except:
                bannedlist = ''
            comment = Comment.objects.filter(Q(movie=movie_id) & ~Q(user__in=bannedlist))
            if comment:
                star = sum([c.star for c in comment]) / len([c.star for c in comment])
                # mm = Movie.objects.get(id=movie_id)
                m.star_personal = round(star, 1)
                m.save()


            else:
                # mm = Movie.objects.get(id=movie_id)
                m.star_personal = 0
                m.save()

        return HttpResponseRedirect(reverse("other_user_account", args=(ban_user.username,)))

class DelBannedView(LoginRequiredMixin, View):
    """
    Del user from bannedlist
    """
    def get(self, request, username):
        user_name = request.COOKIES['username']
        user = User.objects.get(username=user_name)
        ban_user = User.objects.get(username=username)
        bannedlist = Bannedlist.objects.get(user=user)
        bannedlist.banned_user.remove(ban_user)
        bannedlist.save()

        # update star_personal
        all_movie = Movie.objects.all()
        for m in all_movie:
            movie_id = m.id

            try:
                bannedlist = Bannedlist.objects.get(user=user).banned_user.all()
            except:
                bannedlist = ''
            comment = Comment.objects.filter(Q(movie=movie_id) & ~Q(user__in=bannedlist))
            if comment:
                star = sum([c.star for c in comment]) / len([c.star for c in comment])
                # mm = Movie.objects.get(id=movie_id)
                m.star_personal = round(star, 1)
                m.save()

        return HttpResponseRedirect(reverse("other_user_account", args=(ban_user.username,)))

class BannedListView(LoginRequiredMixin, View):
    """
    bannedlist
    """
    def get(self, request):
        username = request.COOKIES['username']
        user = User.objects.get(username=username)
        try:
            banned_id = Bannedlist.objects.get(user=user).banned_user.all()
        except:
            return render(request, 'login/bannedlist.html', {"bannedlist": '', "counts": 0})
        counts = banned_id.count()
        bannedlist = User.objects.filter(Q(id__in= banned_id))
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(bannedlist, 8, request=request)
        bannedlist = p.page(page)

        return render(request, 'login/bannedlist.html', {"bannedlist": bannedlist, "counts": counts})


# 验证码视图类
class GetAuthImg(views.View):
    """获取验证码视图类"""

    def get(self, request):
        data = authcode.get_authcode_img(request)
        print("验证码：", request.session.get("authcode"))
        return HttpResponse(data)


class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=50)
    password = forms.CharField(label='password', widget=forms.PasswordInput())
    email = forms.EmailField(label='email')
    # c_time = forms.DateTimeField(auto_now_add=True)


def Register(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)  # 数据交给form实例化

        if userform.is_valid():  # 验证提交数据的合法性
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            email = userform.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                return render(request, 'login/register.html', {'error_msg': 'Username or Email already exists'})
            Usr = User.objects.create(username=username, password=password, email=email)
            Usr.set_password(password)
            Usr.save()

            return HttpResponseRedirect('../../login/l/')

    else:

        userform = UserForm()

    return render(request, 'login/register.html', {'userform': userform})


class InfoForm(forms.Form):
    info = forms.CharField(label='info', max_length=80)

def ModifyInfo(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/login/profile/')
    if request.method == 'POST':
        infoform = InfoForm(request.POST)
        if infoform.is_valid():
            info = infoform.cleaned_data['info']

            # load block_words
            block_words = pd.read_csv('/login/block-words.txt', header=None)
            info = 'fuck'
            for word in block_words[0]:
                if info.find(word) != -1:
                    info = info.replace(word,'*'*len(word))

            username = request.user
            user = User.objects.get(username=username)
            user.info = 'lll'
            user.save()

            return HttpResponseRedirect('/login/profile/')



    # if not request.session.get('is_login', None):
    #     # 如果本来就未登录，也就没有登出一说
    #     return redirect("/login/")
    # request.session.flush()
    # # 或者使用下面的方法
    # # del request.session['is_login']
    # # del request.session['user_id']
    # # del request.session['user_name']
    # return redirect("/login/")


class LogoutView(View):
    def get(self,request):
        logout(request)
        request.session.flush()
        request.COOKIES.clear()

        return HttpResponseRedirect(reverse("login"))