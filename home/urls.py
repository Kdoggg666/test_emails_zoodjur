from django.contrib import admin
from django.urls import path
from . import views  # from the main app dir import the views

urlpatterns = [
    path('', views.index, name='home'),  # the index function from views file
    path('about/', views.about, name='about'),  # path to the about
]
