from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('add_stock.html', views.add_stock, name="blog-add_stock"),
   	path('delete/<stock_id>', views.delete, name="blog-delete"),
    path('news/', views.news, name='blog-news')
]
