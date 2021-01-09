from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('market/', views.market, name='blog-market'),
    path('news/', views.news, name='blog-news')
]
