from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.login, name=''),

    ##################################### API TESTPAGES ###################################
    path('login',views.login, name = 'login'),
    path('signup',views.signup, name = 'signup'),
    path('logout',views.logout, name='logout'),

    #################################### DEPRECATED #######################################
    path('api_test', views.api_json_test, name=''),
    path('db_test', views.api_json_mysql_check, name='dbtest'),


    ##################################### API ENDPOINTS ####################################
    path('api_login', views.api_login ,name='api_login'),
    path('api_signup', views.api_signup, name = 'api_signup'),
    path('api_logout',views.user_logout, name = 'api_logout'),
    path('api_verifytoken', views.verify_token, name ='api_verifytoken'),
    path('api_changeUserInfo',views.api_changeUserInfo, name = 'api_changeUserInfo'),
    path('api_confirmAccount',views.api_confirmAccount, name = 'api_confirmAccount'),


]