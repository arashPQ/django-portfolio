from django.urls import path
from . import views

app_name='blog'

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('create/', views.create_article, name='create_article'),
]