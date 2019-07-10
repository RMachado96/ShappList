from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('products', views.products, name='products'),
    path('lists', views.lists, name='lists'),
    path('dashboard',views.dashboard, name = 'dashboard'),
    path('add_list',views.add_list, name = 'add_list'),
    path('settings',views.settings, name = 'settings'),
    path('edit_settings',views.edit_settings, name = 'edit_settings'),
    path('individual_list',views.individual_list, name = 'individual_list'),

]