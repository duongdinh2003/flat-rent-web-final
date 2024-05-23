from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('search-nearby/', views.search_nearby, name='search_nearby'),
]