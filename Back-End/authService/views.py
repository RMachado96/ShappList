from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import JsonResponse
from django.db import connection, transaction
from random import randint
from django.core.mail import send_mail
from . import token
import sys
import json
import hashlib
import base64
import time


# Create your views here.

def login(request):
    template = loader.get_template('authService/login.html')

    context = {
            'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))

def signup(request):
    template = loader.get_template('authService/signup.html')

    context = {
            'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))


def logout(request):
    template = loader.get_template('authService/logout.html')

    context = {
            'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))

def api_json_test(request):
    if(request.method=="GET"):
        data = {
            'test_field' : 'GET method received',
        }
        return JsonResponse(data)

    elif(request.method=="POST"):
        dict_data = json.loads(request.body.decode('utf-8'))
        print(dict_data)

        temp_username = dict_data['username']
        temp_password = dict_data['password']

        data = {
            'username' : temp_username,
            'password' : temp_password
        }
        return JsonResponse(data)
    else:
        data = {
            'wait' : 'cant identify request'
        }
        return JsonResponse(data)

def api_json_mysql_check(request):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    #t = Context({'results': rows})
    print(rows)
    print(type(rows))
    data = {'test':'test'}

    return JsonResponse(data)

################################################ LOGIN ################################################
def api_login(request):

    responseData = {}
    if(request.method =="POST"):

        dict_data = json.loads(request.body.decode('utf-8'))
        temp_email = dict_data['email']
        temp_password = dict_data['password']


        userID = check_info_query(temp_email,temp_password)

        if(not userID):
            responseData['updatedDefaultList'] = False
            responseData['status'] = 400
            responseData['message'] = 'User creds wrong '

        elif(userID):
            temp_val = query_getUserDefaultList(userID)
            if( temp_val != 0):
                responseData['updatedDefaultList'] = True
                responseData['defaultList'] = temp_val
            else:
                responseData['updatedDefaultList'] = False

            responseData['status'] = 200
            responseData['message'] = 'User creds ok '
            responseData['token'] = create_token(temp_email,userID)

        else:
            print('You should never get here ')

    else:
        responseData['status'] = 500
        responseData['message'] = 'Not POST '

    return JsonResponse(responseData)

def query_getUserDefaultList(userID):
    query = '''SELECT defaultList FROM users_extended WHERE userID = '''+str(userID)+''';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(cursor_id.rowcount > 0):
        return rows_id[0][0]
    else:
        return 0

################################################ SIGN UP ################################################

def api_signup(request):

    responseData = {}
    dict_data = json.loads(request.body.decode('utf-8'))
    temp_username = dict_data['username']
    temp_password = dict_data['password']
    temp_email = dict_data['email']
    temp_phoneNum = dict_data['phoneNum']
    new_data = {}

    if(request.method =="POST"):
        if(not query_checkIfUserWithMailOrPw(temp_email,temp_phoneNum)):

            if(create_user(temp_username,temp_password,temp_email)):
                print('Added user to table users')
                new_data = get_user_by_email(temp_email)

                if(create_user_extended(new_data['userID'],temp_email,temp_phoneNum)):
                    responseData['status'] = 200
                    responseData['message'] = "User succesfully created"
                    responseData['token'] = create_token(temp_username, new_data['userID'])
                    temp_ver_token = generateHash(temp_username, temp_email)
                    if(query_addVerificationTokenToDatabase(temp_ver_token, new_data['userID'])):
                        support_sendEmail(temp_email, temp_ver_token, temp_username)

                else:
                    if(delete_user(new_data['userID'])):
                        responseData['status'] = 400
                        responseData['message'] = "Could not create user extended "
            else:
                responseData['status'] = 400
                responseData['message'] = "Could not create user "
        elif(query_checkIfUserWithMailOrPw(temp_email,temp_phoneNum)):
            responseData['status'] = 300
            responseData['message'] = "User creds already exist "

    else:
        responseData['status'] = 500
        responseData['message'] = 'Not POST '


    return JsonResponse(responseData)

def query_addVerificationTokenToDatabase(token, userID):
    query = '''INSERT INTO verificationTokensTable VALUES(NULL,''' + str(userID)+ ''',"''' + token + '''",0);'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(cursor_id.rowcount > 0):
        return True
    else:
        return False

def query_checkIfUserWithMailOrPw(email,phoneNum):

    query = ''' SELECT EXISTS ( SELECT 1 FROM users_extended WHERE userMail = "'''+email+'''" OR phoneNum = '''+str(phoneNum)+''');'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(rows_id[0][0] == 1):
        return True
    else:
        return False



def support_sendEmail(email, token, username):
    print("New request to send email...")
    subject = "ShappList - Confirmação de conta"
    message = "Bem vindo " + username + ", a seguir encontra-se o link que deverá ser utilizado para confirmar a sua nova conta na ShappList: https://shapplist.pythonanywhere.com/api/authServices/api_confirmAccount?token=" + token + "\n"
    selfEmail = "noreply@shapplist.com"
    targetEmail = email

    send_mail(subject,
            message,selfEmail,
            [targetEmail],
            fail_silently=False,
            )
    print("Email sent...")



def rand_numb(min_prov, max_prov):

    rand_int = randint(min_prov, max_prov)

    return rand_int


def curr_unix():
    return int(time.time())


def hf_sha512(unhashed_str):
    hasher = hashlib.sha3_512()

    hasher.update(str.encode(unhashed_str))
    token = hasher.hexdigest()
    return(token)



def generateHash(username, email):

    finalString = str(rand_numb(111,999)) + email + str(curr_unix()) + username + str(rand_numb(111,999))

    finalHash = hf_sha512(finalString)

    print(finalHash)
    return(finalHash)


def api_confirmAccount(request):
    temp_ver_token = request.GET.get('token', 'none')
    print(temp_ver_token)
    if(temp_ver_token != 'none'):
        if(query_confirmAccount(temp_ver_token)):
            template = '/products'
        else:
            template = '/login'
    else:
        template = '/login'

    context = {
            'debug' : 'debug'
    }

    return HttpResponseRedirect(template)


def query_confirmAccount(token):
    query = '''UPDATE verificationTokensTable SET isVerified = 1 WHERE verificationToken="''' + token + '''";'''
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(cursor_id.rowcount > 0):
        return True
    else:
        return False

################################################ LOG OUT ################################################

def user_logout(request):

    responseData = {}
    if(request.method =="POST"):

        dict_data = json.loads(request.body.decode('utf-8'))
        temp_token = dict_data['token']

        if(check_token(temp_token)):
            responseData['status'] = 200
            responseData['message'] = 'User successfully logged out '
            delete_token(temp_token)
    else:
        responseData['status'] = 500
        responseData['message'] = 'Not POST '

    return JsonResponse(responseData)

def verify_token(request):

    responseData = {}
    if(request.method =="POST"):
        print('showing decode HERE')
        print(request.body.decode('utf-8'))
        print('######################################################################')
        dict_data = json.loads(request.body.decode('utf-8'))
        temp_token = dict_data['token']

        if(check_token(temp_token)):
            responseData['status'] = 200
            responseData['boolean'] = 'True'
        else:
            responseData['status'] = 200
            responseData['boolean'] = 'False'
    else:
        responseData['status'] = 500
        responseData['message'] = 'Not POST '

    return JsonResponse(responseData)

################################################ CHANGE USER INFO ################################################
def api_changeUserInfo(request):
    dict_data = json.loads(request.body.decode('utf-8'))
    userToken = request.COOKIES.get('token')
    userID = tokenToUser(userToken)
    newField = dict_data['newField']
    fieldType = dict_data['fieldType']
    currentPassword = dict_data['currentPassword']
    data = {}


    if(fieldType == 'username'):
        if(query_confirmUserPassword(userID,currentPassword)):
            if(query_changeUserInfo(newField,'username',userID)):
                data['status'] = 200
                data['message'] = 'Username changed'
            else:
                data['status'] = 400
                data['message'] = 'Query failed'
        else:
            data['status'] = 300
            data['message'] = 'Wrong password'

    elif(fieldType == 'newPassword'):
        if(query_confirmUserPassword(userID,currentPassword)):
            if(query_changeUserInfo(newField,'password',userID)):
                data['status'] = 200
                data['message'] = 'Password changed'
            else:
                data['status'] = 400
                data['message'] = 'Query failed'
        else:
            data['status'] = 300
            data['message'] = 'Wrong password'

    else:
        data['status'] = 400
        data['message'] = 'It crashed my dude'

    return JsonResponse(data)

def query_confirmUserPassword(userID,password):
    query = '''SELECT EXISTS ( SELECT 1 FROM users WHERE uniqueID = '''+str(userID)+''' AND password = "'''+password+'''");'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(rows_id[0][0] == 1):
        return True
    else:
        return False

def query_changeUserInfo(info,field,userID):
    query = '''UPDATE users SET '''+field+'''="'''+info+'''" WHERE uniqueID = '''+str(userID)+''';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(cursor_id.rowcount > 0):
        return True
    else:
        return False

################################################ SUPPORT FUNCTIONS ################################################

def create_token(username,temp_userid):

    temp_token = token.token_style_gen(username)
    curr_time = token.curr_unix()

    cursor_token = connection.cursor()
    token_query = '''INSERT INTO tokensTable(uniqueId,userId,token,unixTime)
                     VALUES(NULL, ''' + str(temp_userid) + ''',"''' + temp_token + '''",''' + str(curr_time) + ''')'''
    cursor_token.execute(token_query)

    return temp_token

def get_user_by_email(email):

    cursor_id = connection.cursor()
    cursor_id.execute("SELECT uniqueId FROM users WHERE userMail = \"" + email + "\"")
    rows_id = cursor_id.fetchall()
    print(rows_id)

    user = {}

    if(not rows_id):
        user['status'] = 400
    else:
        user['status'] = 200
        user['userID'] = rows_id[0][0]

    return user

def check_info_query(email,password):

    query = ''' SELECT IFNULL ( ( SELECT uniqueID FROM users WHERE userMail = "''' + email + '''" AND password = "''' + password + '''"), 0);'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    print(rows_id[0][0])

    if(rows_id[0][0] != 0):
        return rows_id[0][0]
    else:
        print('Couldnt find user')
        return None


def create_user(username,password,email):
    try:
        cursor_insert = connection.cursor()
        insert_query=''' INSERT INTO users(uniqueId,username,password,userMail) VALUES(NULL,"''' + username + '''","''' + password +'''","''' + email +'''");'''

        cursor_insert.execute(insert_query)
        return True

    except Exception as e:
        print('Could not create user')
        print(str(e))
        print(sys.exc_info()[0])
        return False


def create_user_extended(uniqueID,email,phoneNum):

    curr_time = token.curr_unix()
    try:

        cursor_insert = connection.cursor()
        insert_query=''' INSERT INTO users_extended(uniqueID,userID,userMail,phoneNum,emailVerify,signUpDate)
                        VALUES(NULL,''' + str(uniqueID) + ''',"''' + email +'''",''' + str(phoneNum) +''',false,'''+ str(curr_time) + ''')'''

        cursor_insert.execute(insert_query)
        return True

    except:
        print('Could not create user extended')
        print(sys.exc_info()[0])
        return False

def delete_user(uniqueID):
    query = ''' DELETE FROM users WHERE uniqueID = ''' + str(uniqueID) + ''';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)

    if(cursor_id.rowcount > 0):
        return True
    else:
        print('Couldnt create list')
        return False

def delete_token(token):

    cursor_id = connection.cursor()
    cursor_id.execute("DELETE FROM tokensTable WHERE token = \"" + token + "\"")

    return True

def check_token(user_token):

    curr_time = token.curr_unix()
    cursor_id = connection.cursor()
    cursor_id.execute("SELECT token,unixTime FROM tokensTable WHERE token = \"" + user_token + "\"")
    rows_id = cursor_id.fetchall()
    print(rows_id)


    if(not rows_id):
        return False
    elif((int(curr_time) - int(rows_id[0][1])) > 43200):
        delete_token(user_token)
        return False
    else:
        return True

def tokenToUser(token):
    query = ''' SELECT userID FROM tokensTable WHERE token=\'''' + token +'''\';'''
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    query_result = rows_id[0][0]

    return query_result



