from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    ##### APIS ####
    path('api_createList', views.api_createList ,name='api_createList'),
    path('api_addProducts', views.api_addProducts, name='api_addProducts'),
    path('api_getList', views.api_getList ,name='api_getList'),
    path('api_getUserID', views.api_getUserID, name='api_getUserID'),
    path('api_getAllLists', views.api_getAllLists, name='api_getAllLists'),
    path('api_getListProductsByCategory', views.api_getListProductsByCategory, name='api_getListProductsByCategory'),
    path('api_removeProducts', views.api_removeProducts, name ='api_removeProducts'),
    path('api_fillInfo',views.api_fillInfo, name = 'api_fillInfo'),
    path('api_getParticipant',views.api_getParticipant,name ='api_getParticipant'),
    path('api_getUserInvites',views.api_getUserInvites,name = 'api_getUserInvites'),
    path('api_replyToUserInvites',views.api_replyToUserInvites,name = 'api_replyToUserInvites'),
    path('api_deleteList',views.api_deleteList,name = 'api_deleteList'),
    path('api_leaveList',views.api_leaveList,name = 'api_leaveList'),
    path('api_checkIfOwnerOfList', views.api_checkIfOwnerOfList, name = 'api_checkIfOwnerOfList'),
    path('api_getInfoForUsersInList',views.api_getInfoForUsersInList, name = 'api_getInfoForUsersInList'),
    path('api_removeUserFromList', views.api_removeUserFromList, name = 'api_removeUserFromList'),
    path('api_updateDefaultList', views.api_updateDefaultList, name = 'api_updateDefaultList'),

    ##### VIEWS ####
    path('test_createList', views.test_createList, name = 'test_createList'),
    path('test_addProducts', views.test_addProducts ,name = 'test_addProducts'),
    path('test_getList', views.test_getList ,name = 'test_getList'),
]
