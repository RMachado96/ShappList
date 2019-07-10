from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.db import connection, transaction
from . import verifyToken
from . import token



def index(request):
    accept = False
    if(not request.COOKIES.get('')):
        temp_token = request.COOKIES.get('token')
        #accept = verifyToken.verify_token(temp_token) #use when deployed
        if(temp_token != None ):
            accept = check_token(temp_token)

    if(accept):
        template = loader.get_template('pageServer/tempProducts.html')

    else:
        template = loader.get_template('pageServer/index.html')


    context = {
        'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))

def register(request):
    accept = False
    if(not request.COOKIES.get('')):
        temp_token = request.COOKIES.get('token')
        #accept = verifyToken.verify_token(temp_token) #use when deployed
        if(temp_token != None ):
            accept = check_token(temp_token)

    if(accept):
        template = loader.get_template('pageServer/tempProducts.html')

    else:
        template = loader.get_template('pageServer/register.html')


    context = {
        'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))

def login(request):

    accept = False
    if(not request.COOKIES.get('')):
        temp_token = request.COOKIES.get('token')
        #accept = verifyToken.verify_token(temp_token) #use when deployed
        if(temp_token != None ):
            accept = check_token(temp_token)

    if(accept):
        template = loader.get_template('pageServer/tempProducts.html')

    else:
        template = loader.get_template('pageServer/login.html')

    #template = loader.get_template('pageServer/login.html')

    context = {
            'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))

def dashboard(request):

    accept = False
    if(not request.COOKIES.get('')):
        temp_token = request.COOKIES.get('token')
        #accept = verifyToken.verify_token(temp_token) #use when deployed
        if(temp_token != None ):
            accept = check_token(temp_token)

    if(accept):
        template = loader.get_template('pageServer/dashboard.html')

    else:
        template = loader.get_template('pageServer/login.html')


    context = {
        'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))


def products(request):
    accept = False
    if(not request.COOKIES.get('')):
        temp_token = request.COOKIES.get('token')
        #accept = verifyToken.verify_token(temp_token) #use when deployed
        if(temp_token != None ):
            accept = check_token(temp_token)

    if(accept):
        template = loader.get_template('pageServer/tempProducts.html')

    else:
        template = loader.get_template('pageServer/login.html')


    context = {
        'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))

def lists(request):
    accept = False
    if(not request.COOKIES.get('')):
        temp_token = request.COOKIES.get('token')
        #accept = verifyToken.verify_token(temp_token) #use when deployed
        if(temp_token != None ):
            accept = check_token(temp_token)

    if(accept):
        template = loader.get_template('pageServer/lists.html')

    else:
        template = loader.get_template('pageServer/login.html')


    context = {
        'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))

def add_list(request):
    accept = False
    if(not request.COOKIES.get('')):
        temp_token = request.COOKIES.get('token')
        #accept = verifyToken.verify_token(temp_token) #use when deployed
        if(temp_token != None ):
            accept = check_token(temp_token)

    if(accept):
        template = loader.get_template('pageServer/addList.html')

    else:
        template = loader.get_template('pageServer/login.html')


    context = {
        'debug' : 'debug'
    }


    return HttpResponse(template.render(context, request))

def settings(request):
    accept = False
    if(not request.COOKIES.get('')):
        temp_token = request.COOKIES.get('token')
        #accept = verifyToken.verify_token(temp_token) #use when deployed
        if(temp_token != None ):
            accept = check_token(temp_token)

    if(accept):
        template = loader.get_template('pageServer/settings.html')

    else:
        template = loader.get_template('pageServer/login.html')


    context = {
        'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))

def individual_list(request):
    accept = False
    if(not request.COOKIES.get('')):
        temp_token = request.COOKIES.get('token')
        #accept = verifyToken.verify_token(temp_token) #use when deployed
        if(temp_token != None ):
            accept = check_token(temp_token)

    if(accept):
        template = loader.get_template('pageServer/individualList.html')

    else:
        template = loader.get_template('pageServer/login.html')


    context = {
        'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))

def edit_settings(request):
    accept = False
    if(not request.COOKIES.get('')):
        temp_token = request.COOKIES.get('token')
        #accept = verifyToken.verify_token(temp_token) #use when deployed
        if(temp_token != None ):
            accept = check_token(temp_token)

    if(accept):
        template = loader.get_template('pageServer/editSettings.html')

    else:
        template = loader.get_template('pageServer/login.html')


    context = {
        'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))



def check_token(user_token):

    curr_time = token.curr_unix()
    cursor_id = connection.cursor()
    cursor_id.execute("SELECT token,unixTime FROM tokensTable WHERE token = \"" + user_token + "\"")
    rows_id = cursor_id.fetchall()
    print(rows_id)


    if(not rows_id):
        return False
    elif((int(curr_time) - int(rows_id[0][1])) > 43200):
        #delete_token(user_token)
        return False
    else:
        return True
