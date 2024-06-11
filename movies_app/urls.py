from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('home/', views.home, name='home'),
    path('add/', views.add_movie, name='add_movie'),
    path('<int:movie_id>/edit/', views.edit_movie, name='edit_movie'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_id>/review/', views.add_review, name='add_review'),
    path('category/', views.category_movies, name='category_movies'),
    path('my-movies/', views.user_movies, name='user_movies'),
    path('delete-movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('search_result/', views.search_movies, name='search_movies'),
    path('category/<int:category_id>/', views.category_movies, name='category_movies_with_id'),


]
