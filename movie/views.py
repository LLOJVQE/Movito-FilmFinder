from django.shortcuts import render
from login.models import User
from login.forms.login import formAuth

from django import views
from django.contrib import auth
from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import (
    render, redirect, reverse, HttpResponse, HttpResponseRedirect
)
from django.db.models import Q
from django.views.generic.base import View
from movie.models import Movie, Tag
import pandas as pd
from operator import itemgetter
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django import forms
from login.models import Comment,Bannedlist
import os
#
def IndexView(request):
    try:
        user = request.user
    except:
        user = None


    # user = request.session.get('user', False)
    movie_popular = Movie.objects.all().order_by('-comment_nums','title')[:12]
    movie_top_rate = Movie.objects.all().order_by('-star_personal','title')[:12]
    # movies = movie_popular | movie_top_rate

    # star_dic = dict()
    # for m in movies:
    #     movie_id = m.id
    #
    #     try:
    #         bannedlist = Bannedlist.objects.get(user=user).banned_user.all()
    #     except:
    #         bannedlist = ''
    #     comment = Comment.objects.filter(Q(movie=movie_id) & ~Q(user__in=bannedlist))
    #     if comment:
    #         star = sum([c.star for c in comment]) / len([c.star for c in comment])
    #         star_dic[movie_id] = round(star,1)
    #     else:
    #         star_dic[movie_id] = 0


    return render(request, 'movie/index.html', {'user': user,"movie_popular": movie_popular,
                                                "movie_top_rate": movie_top_rate})


class MovieForm(forms.Form):
    title = forms.CharField(label='title', max_length=50)


class SearchView(LoginRequiredMixin,View):
    def get(self, request,keywords):
        # search_keywords = request.GET.get('keywords', '')
        search_keywords = keywords
        if not search_keywords:
            search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            movies = Movie.objects.filter\
                (Q(title__icontains=search_keywords) | Q(info__icontains=search_keywords) | Q(director__icontains=search_keywords)|Q(genres_text__contains=search_keywords)).order_by('-star_personal','title')
            counts = movies.count()

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
            #         star_dic[movie_id] = round(star,1)
            #     else:
            #         star_dic[movie_id] = 0

            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(movies, 8, request=request)
            movies = p.page(page)
        else:

            return HttpResponseRedirect('/movie/')

        return render(request, 'movie/search_result.html',
                      {"movies": movies, "search_keywords": search_keywords, "counts": counts})

class SearchByGenresView(LoginRequiredMixin,View):
    def get(self, request,keywords):
        # search_keywords = request.GET.get('keywords', '')
        search_keywords = keywords
        if not search_keywords:
            search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            movies = Movie.objects.filter\
                (Q(director__contains=search_keywords)|Q(genres_text__contains=search_keywords) ).order_by('-star_personal','title')
            counts = movies.count()

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
            #         star_dic[movie_id] = round(star,1)
            #     else:
            #         star_dic[movie_id] = 0

            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(movies, 8, request=request)
            movies = p.page(page)
        else:

            return HttpResponseRedirect('/movie/')

        return render(request, 'movie/search_result.html',
                      {"movies": movies, "search_keywords": search_keywords, "counts": counts})


class MovieDetailView(LoginRequiredMixin,View):
    """
    Movie Details
    """
    def get(self, request, movie_id, genre_id):
        """
        主体部分
        """
        movie = Movie.objects.get(id=movie_id)
        username = request.user
        user = User.objects.get(username=username)
        if_in_wishlist = movie in user.wishlist.all()
        if_commented = Comment.objects.filter(movie=movie_id,user=user)
        try:
            bannedlist = Bannedlist.objects.get(user=user).banned_user.all()
        except:
            bannedlist = ''
        comments = Comment.objects.filter(Q(movie=movie_id) & ~Q(user__in=bannedlist))
        if comments:
            star = round(sum([c.star for c in comments]) / len([c.star for c in comments]),1)
        else:
            star = 0
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(comments, 8, request=request)
        comments = p.page(page)
        """
        Recommendation部分
        """
        request_path = request.path
        q = {} #筛选条件的字典

        genre_list = Comment.objects.filter(Q(user=user)).values('movie').values('movie__genres','movie__genres__name').distinct()
        if genre_id == '50':
            # all the genres
            pass
        else:
            # select one genres
            genre = Tag.objects.get(id=int(genre_id))
            commented_movies_genres = Comment.objects.filter(Q(user=user)).values('movie').values('movie__genres__id') # 感兴趣的genreid
            q['genres__in'] = [genre_id,]
            # request_path = request_path.split('-')[0]+str(genre_id)
        if genre_id == '50':
            # for g in genre_list.all()
            recommendation_movies = Movie.objects.filter(genres__in=genre_list.all().values('movie__genres'))
        else:
            recommendation_movies = Movie.objects.filter(**q).order_by('-star','title')[:20]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p_2 = Paginator(recommendation_movies, 3, request=request)
        recommendation_movies = p_2.page(page)

        """
        movie rate
        """
        # movies = Movie.objects.filter(**q).order_by('star','title')[:20]
        # star_dic = dict()
        # for m in movies:
        #     movie_id = m.id
        #     username = request.user
        #     user = User.objects.get(username=username)
        #     try:
        #         bannedlist = Bannedlist.objects.get(user=user).banned_user.all()
        #     except:
        #         bannedlist = ''
        #     comment = Comment.objects.filter(Q(movie=movie_id) & ~Q(user__in=bannedlist))
        #     if comment:
        #         star = round(sum([c.star for c in comment]) / len([c.star for c in comment]),1)
        #         star_dic[movie_id] = round(star,1)
        #     else:
        #         star_dic[movie_id] = 0


        return render(request, 'movie/details.html', {"movie": movie, "comments": comments,
                                                      'if_in_wishlist': if_in_wishlist, "if_commented": if_commented,
                                                      "star":star, "recommendation_movies": recommendation_movies,
                                                      "current_url":request_path,"genre_list": genre_list})




class Add_wishlist(LoginRequiredMixin, View):
    def get(self, request, movie_id):
        username = request.user
        user = User.objects.get(username=username)
        movie = Movie.objects.get(id=movie_id)
        user.wishlist.add(movie)
        user.save()

        # response = render(request,'url')
        # response.set_cookie('url', request.get_full_path())

        # return HttpResponse({'You have added it to your wishlist!'})
        return HttpResponseRedirect(reverse("detail", args=(movie_id,50)), {"user": user,"movie": movie})

class CommentForm(forms.Form):
    movie_id = forms.CharField(required=True)
    rate = forms.IntegerField(required=True)
    content = forms.CharField(required=False)


class CommentView(LoginRequiredMixin,View):

    def post(self, request):
        add_form = CommentForm(request.POST)
        if add_form.is_valid():
            content = request.POST.get("content", "")
            star = int(request.POST.get("rate",""))
            movie_id = request.POST.get("movie_id", "")
            movie = Movie.objects.get(id=movie_id)
            # load block_words
            module_dir = os.path.dirname(__file__)
            file_path = os.path.join(module_dir, 'block-words.txt')  # full path to text.
            block_words = pd.read_csv(file_path, header=None)
            for word in block_words[0]:
                if content.find(word) != -1:
                    content = content.replace(word, '*' * len(word))
            comment = Comment(user=request.user, star=star, content=content, movie=movie)
            comment.save()


            movie.comment_nums += 1
            movie.star = (movie.star*(movie.comment_nums-1) + star)/movie.comment_nums
            movie.save()
            return HttpResponseRedirect(reverse("detail", args=(movie_id,50)))
        else:
            return HttpResponse('Please review again.')


# def Logout(request):
#     logout(request)
#     request.session.flush()
#     # request.COOKIES.clear()
#     request.session['user'] = ''
#
#     # request.session.flush()
#     return HttpResponseRedirect('/login/l')

# class LogoutView(View):
#     def get(self,request):
#         logout(request)
#         request.session.flush()
#         return HttpResponseRedirect('/movie/')
