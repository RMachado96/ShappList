from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('api_getProducts', views.api_getProducts ,name='api_getProducts'),
    path('api_getProductLowestPrice', views.api_getProductLowestPrice, name = 'api_getProductLowestPrice'),
    path('api_getProductsWithDiscount', views.api_getProductsWithDiscount, name = 'api_getProductsWithDiscount'),
]
