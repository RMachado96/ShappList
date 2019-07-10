from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.db import connection, transaction
import json

def test_createList(request):

    template = loader.get_template('listService/testList.html')

    context = {
            'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))

def test_getList(request):
    template = loader.get_template('listService/testgetlist.html')

    context = {
            'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))

########## CREATE LISTS ##########
def api_getUserID(request):
    userToken = request.COOKIES.get('token')
    userID = tokenToUser(userToken)

    if(userID):
        data = {'status' : 'success', 'userID' : userID}
    else:
        print('Couldnt get user ID')
        data = {'status' : 'failed'}

    return JsonResponse(data)

def api_createList(request):

    dict_data = json.loads(request.body.decode('utf-8'))
    listname = dict_data['listname']
    defaultLevel = dict_data['defaultLevel']
    #userToken = dict_data['token']
    userToken = request.COOKIES.get('token')
    print(userToken)
    userID = tokenToUser(userToken)
    noLists = query_checkIfUserInAnyList(userID)

    if(createList(listname,userID,defaultLevel)):
        print('List created')
        if(not noLists):
            if(setDefaultListOnCreate(userID)):
                data = {'status' : 'success', 'updatedDefaultList' : True, 'defaultList' : query_getListByParticipant(userID)}
            else:
                data = {'status' : 'failed'}
        else:
            data = {'status' : 'success', 'updatedDefaultList' : False}
    else:
        data = {'status' : 'failed'}

    return JsonResponse(data)

def tokenToUser(token):
    query = ''' SELECT userID FROM tokensTable WHERE token=\'''' + token +'''\';'''
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    query_result = rows_id[0][0]

    return query_result

def createList(listName,userID,defaultLevel):

    query = ''' INSERT INTO user_list VALUES(NULL,''' + str(userID) + ''',\'''' + listName + '''\',''' + str(defaultLevel) +''');'''
    print('query inser into userlist')
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)

    if(addParticipant(getListId(userID),userID)):
        print('added participant')
        if(cursor_id.rowcount > 0):
            return True
        else:
            print('Couldnt create list')
            return False
    else:
        return False

def getListId(ownerID):
    query = ''' SELECT MAX(uniqueID) FROM user_list WHERE ownerID= ''' + str(ownerID) + ''';'''
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    listId = rows_id[0][0]

    if(cursor_id.rowcount > 0):
        return listId
    else:
        print('Couldnt create list')

def query_checkIfUserInAnyList(userID):
    query = '''SELECT EXISTS(SELECT 1 from user_list_participants WHERE userID = ''' + str(userID) + ''');'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(rows_id[0][0] == 1):
        return True
    else:
        return False

def query_getListByParticipant(userID):
    query = '''SELECT listID from user_list_participants WHERE userID = '''+str(userID)+''' ;'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(cursor_id.rowcount > 0):
        return rows_id[0][0]
    else:
        print('Could not find list')

def query_updateDefaultList(listID,userID):
    query = ''' UPDATE users_extended SET defaultList =''' + str(listID) + ''' WHERE userID = '''+ str(userID)+''';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(cursor_id.rowcount > 0):
        return True
    else:
        return False
        print('Could not update default list')

def query_updateDefaultListOnDelete(oldListID):
    query = ''' UPDATE users_extended SET defaultList = 0  WHERE defaultList = '''+ str(oldListID)+''';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(cursor_id.rowcount > 0):
        return True
    else:
        return False
        print('Could not delete list')

def setDefaultListOnCreate(userID):

    listID = query_getListByParticipant(userID)

    if(query_updateDefaultList(listID,userID)):
        return True
    else:
        return False

def addParticipant(listID,userID):
    # add level 1- suggestions if possible
    # level 2 - control all
    query = '''INSERT INTO  user_list_participants VALUES(NULL,''' +str(listID)+''',''' +str(userID)+''',2);'''
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)

    if(cursor_id.rowcount > 0):
        return True
    else:
        print('Couldnt add participant')
        return False

########## DELETE LIST ##########
#verifications already made to see if you are the owner and therefore have permission to fully delete list

def api_deleteList(request):
    dict_data = json.loads(request.body.decode('utf-8'))
    listID = dict_data['listID']
    data = {}

    if(query_deleteListByID(listID)):
        if(query_updateDefaultListOnDelete(listID)):
            data['status'] = 200
            data['message'] = 'List successfully deleted and defaultLists changed to 0'
        else:
            data['status'] = 400
            data['message'] = 'Could not delete list'
    else:
        data['status'] = 400
        data['message'] = 'Could not delete list'

    return JsonResponse(data)

def query_deleteListByID(listID):
    query = ''' DELETE FROM user_list WHERE uniqueID = '''+str(listID)+''';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)

    if(cursor_id.rowcount > 0):
        return True
    else:
        print('Couldnt delete list')
        return False

########## LEAVE LIST ##########
#verifications already made to see if you are just a participant and therefore can only leave list

def api_leaveList(request):
    dict_data = json.loads(request.body.decode('utf-8'))
    listID = dict_data['listID']
    userToken = request.COOKIES.get('token')
    userID = tokenToUser(userToken)
    data = {}

    if(query_leaveList(listID,userID)):
        data['status'] = 200
        data['message'] = 'Successfully left list'
    else:
        data['status'] = 400
        data['message'] = 'Could not leave list'

    return JsonResponse(data)

def query_leaveList(listID,userID):
    query = ''' DELETE FROM user_list_participants WHERE listID = '''+str(listID)+''' AND userID = '''+str(userID)+''';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)

    if(cursor_id.rowcount > 0):
        return True
    else:
        print('Couldnt leave list')
        return False

def api_removeUserFromList(request):
    dict_data = json.loads(request.body.decode('utf-8'))
    listID = dict_data['listID']
    userID = dict_data['userID']
    data={}

    if(not query_checkIfRemovingOwner(listID,userID)):
        if(query_removeUserFromList(listID,userID)):
            data['status'] = 200
            data['message'] = 'Successfully removed from list'
        else:
            data['status'] = 400
            data['message'] = 'Could not leave list'

    elif(query_checkIfRemovingOwner(listID,userID)):
        data['status'] = 300
        data['message'] = 'Trying to delete owner of list'
    else:
        data['status'] = 400
        data['message'] = 'Error checking owner'


    return JsonResponse(data)

def query_checkIfRemovingOwner(listID,userID):
    query = '''SELECT EXISTS ( SELECT 1 FROM user_list where ownerID = '''+str(userID)+''' AND uniqueID = '''+str(listID)+''');'''
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    if(rows_id[0][0] == 1):
        return True
    else:
        return False

def query_removeUserFromList(listID,userID):
    query = '''DELETE FROM user_list_participants WHERE listID = '''+str(listID)+''' AND userID = '''+str(userID)+''' ;'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)

    if(cursor_id.rowcount > 0):
        return True
    else:
        print('Couldnt delete from list')
        return False

########## MODIFY PRODUCTS IN LIST ##########
def test_addProducts(request):

    template = loader.get_template('listService/testAddProducts.html')

    context = {
            'debug' : 'debug'
    }

    return HttpResponse(template.render(context, request))

def api_addProducts(request):
    dict_data = json.loads(request.body.decode('utf-8'))
    listID = dict_data['listID']
    productID = dict_data['productID']
    tag = dict_data['tag']
    #productQuantity = dict_data['productQuantity']
    productQuantity = 1
    userToken = request.COOKIES.get('token')
    addedBy = tokenToUser(userToken)

    if(not query_verifyIfProductInList(listID, productID)):
        if(addProduct(listID,productID,productQuantity,addedBy)):
            data = {'status' : 'success'}
        else:
            data = {'status' : 'failed'}
    else:
        if(tag): # tag is a boolean, true = add quantity // false = remove quantity
            if(addQuantityToProduct(listID, productID)):
                data = {'status' : 'success'}
            else:
                data = {'status' : 'failed'}
        else:
            if(removeQuantityFromProduct(listID, productID)):
                data = {'status' : 'success'}
            else:
                data = {'status' : 'failed'}


    return JsonResponse(data)

def api_removeProducts(request):
    dict_data = json.loads(request.body.decode('utf-8'))
    listID = dict_data['listID']
    productID = dict_data['productID']
    userToken = request.COOKIES.get('token')
    userID = tokenToUser(userToken)

    if(checkUserLevel(userID,listID) == 2):
        if(removeProduct(listID,productID)):
            data = {'status' : 'success'}
        else:
            data = {'status' : 'failed'}
    else:
        print('User level too low')
        data = {'status' : 'failed'}

    return JsonResponse(data)

def removeProduct(listID,productID):
    query = '''DELETE FROM list_content WHERE listID = ''' + str(listID) + ''' AND productID = ''' + str(productID) + ''';'''
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)

    if(cursor_id.rowcount > 0):
        return True
    else:
        print('Couldnt remove product')
        return False

def checkUserLevel(userID,listID):

    query = ''' SELECT userLevel FROM user_list_participants WHERE userID = ''' + str(userID) + ''' AND listID = ''' + str(listID) +''';'''
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(cursor_id.rowcount > 0):
        return rows_id[0][0]
    else:
        print('Couldnt find userlevel')
        return False

def addProduct(listID,productID,productQuantity,addedBy):
    query = ''' INSERT INTO list_content VALUES(NULL,''' + str(listID) + ''',''' + str(productID) + ''',''' + str(productQuantity) +''','''+ str(addedBy)+''');'''
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)

    if(cursor_id.rowcount > 0):
        return True
    else:
        print('Couldnt add product')
        return False

def addQuantityToProduct(listID, productID):
    query = 'UPDATE list_content SET productQuantity = productQuantity + 1 WHERE listID = ' + str(listID) + ' and productID = ' + str(productID) + ';'
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)

    if(cursor_id.rowcount > 0):
        return True
    else:
        print('Couldnt add product')
        return False

def removeQuantityFromProduct(listID, productID):
    query = 'UPDATE list_content SET productQuantity = productQuantity - 1 WHERE listID = ' + str(listID) + ' and productID = ' + str(productID) + ';'
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)

    if(cursor_id.rowcount > 0):
        return True
    else:
        print('Couldnt remove product')
        return False

def query_verifyIfProductInList(listID, productID):
    query = 'SELECT EXISTS(SELECT * from list_content WHERE listID = ' + str(listID) + ' and productID = ' + str(productID) + ');'
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(rows_id[0][0] == 1):
        return True
    else:
        return False

########## GET LISTS ##########
def api_getList(request):
    #dict_data = json.loads(request.body.decode('utf-8'))
    userToken = request.COOKIES.get('token')
    userID = tokenToUser(userToken)
    listDict = getLevel2Lists(userID)

    return JsonResponse(listDict)

def getLevel2Lists(userID):
    query = ''' SELECT ul.uniqueID,ul.listName FROM user_list ul INNER JOIN user_list_participants ulp ON ul.uniqueID = ulp.listID WHERE ulp.userID =''' + str(userID) + ''' AND ulp.userLevel=2;'''
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    returnList = []

    for i in rows_id:
        returnList.append(i[0])

    listCount = len(returnList)
    listDict = {'listCount' : listCount}
    listNumber = 1

    if(listCount > 0):
        tempDict = {}
        for i in rows_id:
            tempDict2 = {'listID' : i[0], 'listName' : i[1]}
            tempDict['list' + str(listNumber)] = tempDict2
            listNumber +=1
        listDict['lists'] = tempDict

    return listDict

def api_getAllLists(request):
    userToken = request.COOKIES.get('token')
    userID = tokenToUser(userToken)
    listsDict = query_getAllLists(userID)

    return JsonResponse(listsDict)

def api_checkIfOwnerOfList(request):

    dict_data = json.loads(request.body.decode('utf-8'))
    userToken = request.COOKIES.get('token')
    userID = tokenToUser(userToken)
    listID = dict_data['listID']
    data = {}
    print(userID)
    print(listID)

    if(query_checkIfOwnerOfListOnLoad(listID,userID)):
        data['status'] = 200
        data['message'] = 'Query worked as intended'
        data['owner'] = True
    elif(not query_checkIfOwnerOfListOnLoad(listID,userID)):
        data['status'] = 200
        data['message'] = 'Query worked as intended'
        data['owner'] = False
    else:
        data['status'] = 400
        data['message'] = 'Query failed'

    return JsonResponse(data)

def query_checkIfOwnerOfListOnLoad(listID,userID):
    query = '''SELECT EXISTS ( SELECT 1 FROM user_list WHERE uniqueID = '''+str(listID)+''' AND ownerID = '''+str(userID)+''');'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    print("######################################################################")
    print(rows_id)

    if(rows_id[0][0] == 1):
        return True
    else:
        return False

def query_getAllLists(userID):
    query = ''' SELECT ul.uniqueID,ul.listName FROM user_list ul INNER JOIN user_list_participants ulp ON ul.uniqueID = ulp.listID WHERE ulp.userID =''' + str(userID) + ''';'''
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    returnDict = {}
    listCount = 0

    for i in rows_id:
        listCount += 1

    returnDict['listCount'] = listCount


    if(listCount > 0):
        tempDict = {}
        tempParticipantsDict = {}
        for i in range(listCount):
            tempDict['list' + str(i)] = {'listId' : rows_id[i][0] , 'listName' : rows_id[i][1]}

        for j in range(listCount):
            tempParticipantsDict['list' + str(j)] = { 'participants' : query_getUsersInList(tempDict['list'+str(j)]['listId'],userID) }
            tempParticipantsDict['list' + str(j)]['isOwner'] = query_checkIfOwnerOfList(userID,tempDict['list'+str(j)]['listId'])


        returnDict['lists'] = tempDict
        returnDict['listParticipants'] = tempParticipantsDict

    print("FINISHED FOR")
    print(returnDict)

    return(returnDict)

def query_checkIfOwnerOfList(userID,listID):
    query = ''' SELECT EXISTS ( SELECT 1 FROM user_list WHERE uniqueID ='''+str(listID)+''' AND ownerID = '''+str(userID)+''');'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    print(rows_id[0][0])

    if(rows_id[0][0] == 1):
        return True
    else:
        print('Is not owner')
        return False

def query_getUsersInList(listID,userID):

    print("#############################")
    print(listID)
    #SELECT u.username FROM users u INNER JOIN user_list_participants ulp ON u.uniqueID = ulp.userID where ulp.listID = 19 AND u.uniqueID != 5;
    query = '''SELECT u.username FROM users u INNER JOIN user_list_participants ulp ON u.uniqueID = ulp.userID where ulp.listID = '''+str(listID)+''' AND u.uniqueID != ''' + str(userID)+''';'''
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    temp_list = []

    if(cursor_id.rowcount > 0):
        for i in rows_id:
            temp_list.append(i[0])

    return temp_list

def api_getListProductsByCategory(request):
    print(request)
    dict_data = json.loads(request.body.decode('utf-8'))
    listID = dict_data['listID']
    userToken = request.COOKIES.get('token')
    userID = tokenToUser(userToken)

    retDict = query_getListProductsByCategory(listID)

    return JsonResponse(retDict)

def query_getListProductsByCategory(listID):

    query = 'SELECT lc.productID, lc.productQuantity,pr.itemName,pr.itemCategory FROM list_content lc INNER JOIN products pr ON lc.productID= pr.uniqueID WHERE lc.listID = ' + str(listID) + ';'
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    itemPrefix = 'item'
    actualRetDict = {}

    actualRetDict['totalItems'] = len(rows_id)
    actualRetDict['listName'] = query_getListNameByID(listID)
    retDict = {}
    ###########################################
    retDict['Frutas e Legumes'] = {}
    retDict['Congelados'] = {}
    retDict['Bebidas'] = {}
    retDict['Mercearia'] = {}
    retDict['Lacticínios'] = {}
    retDict['Carne e Peixe'] = {}
    retDict['Bolachas e Doces'] = {}
    retDict['Charcutaria e Queijos'] = {}
    ###########################################

    ###########################################
    countDict = {}
    countDict['FL'] = 0
    countDict['CL'] = 0
    countDict['BD'] = 0
    countDict['MC'] = 0
    countDict['LT'] = 0
    countDict['CP'] = 0
    countDict['BS'] = 0
    countDict['CQ'] = 0
    ###########################################

    for i in rows_id:

        tempDict = {}
        tempDict['itemID'] = i[0]
        tempDict['itemQuantity'] = i[1]
        tempDict['itemName'], shitVar = treatBrand(i[2])
        tempDict['pricesStores'] = query_getItemPricesAndStoresByName(tempDict['itemName'])

        if(i[3] == 'Frutas e Legumes'):
            retDict['Frutas e Legumes'][itemPrefix + str(countDict['FL'])] = tempDict
            countDict['FL'] = countDict['FL'] + 1


        elif(i[3] == 'Congelados'):
            retDict['Congelados'][itemPrefix + str(countDict['CL'])] = tempDict
            countDict['CL'] = countDict['CL'] + 1

        elif(i[3] == 'Bebidas'):
            retDict['Bebidas'][itemPrefix + str(countDict['BD'])] = tempDict
            countDict['BD'] = countDict['BD'] + 1

        elif(i[3] == 'Mercearia'):
            retDict['Mercearia'][itemPrefix + str(countDict['MC'])] = tempDict
            countDict['MC'] = countDict['MC'] + 1

        elif(i[3] == 'Lacticínios'):
            retDict['Lacticínios'][itemPrefix + str(countDict['LT'])] = tempDict
            countDict['LT'] = countDict['LT'] + 1

        elif(i[3] == 'Carne e Peixe'):
            retDict['Carne e Peixe'][itemPrefix + str(countDict['CP'])] = tempDict
            countDict['CP'] = countDict['CP'] + 1

        elif(i[3] == 'Bolachas e Doces'):
            retDict['Bolachas e Doces'][itemPrefix + str(countDict['BS'])] = tempDict
            countDict['BS'] = countDict['BS'] + 1

        elif(i[3] == 'Charcutaria e Queijos'):
            retDict['Charcutaria e Queijos'][itemPrefix + str(countDict['CQ'])] = tempDict
            countDict['CQ'] = countDict['CQ'] + 1

        else:
            print('something went wrong')
            #you shouldnt be here anyway


    actualRetDict['itemCounters'] = countDict
    actualRetDict['productCatList'] = retDict

    print(actualRetDict)

    return actualRetDict

def query_getItemPricesAndStoresByName(itemName):
    #SELECT itemPrice,storeID from products where itemName like 'Kiwi%';
    query = '''SELECT itemPrice,storeID FROM products WHERE itemName LIKE \''''+itemName+'''%\';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    ret_arr = {}
    count = 0
    storeArr = []
    tempStoreDict = {}
    defaultStoresArr = [1, 2, 3]
    temp_dict = {}


    '''if(cursor_id.rowcount > 0):

        temp_dict = {}
        for i in rows_id:
            temp_dict['storePrice'+str(count)] = {}
            temp_dict['storePrice'+str(count)]['itemPrice'] = i[0]
            temp_dict['storePrice'+str(count)]['storeID'] = i[1]
            count +=1

        ret_arr = temp_dict

        return ret_arr'''

    if(cursor_id.rowcount > 0):
        for i in range(len(rows_id)):
            tempStoreDict[rows_id[i][1]] = i
            storeArr.append(rows_id[i][1])

    print(tempStoreDict)
    print(storeArr)


    '''if(cursor_id.rowcount > 0):
        for i in range(2):
            temp_dict['storePrice'+str(count)] = {}
            temp_dict['storePrice'+str(count)]['itemPrice'] = i[0]
            temp_dict['storePrice'+str(count)]['storeID'] = i[1]
            count +=1'''

    ######
    # Set pingoDoce
    temp_dict['storePrice'+str(count)] = {}
    temp_dict['storePrice'+str(count)]['storeID'] = defaultStoresArr[0]
    if(temp_dict['storePrice'+str(count)]['storeID'] in storeArr):
        temp_dict['storePrice'+str(count)]['itemPrice'] = rows_id[tempStoreDict[1]][0]
        temp_dict['storePrice'+str(count)]['exists'] = True
    else:
        temp_dict['storePrice'+str(count)]['itemPrice'] = None
        temp_dict['storePrice'+str(count)]['exists'] = False

    count +=1

    temp_dict['storePrice'+str(count)] = {}
    temp_dict['storePrice'+str(count)]['storeID'] = defaultStoresArr[1]
    if(temp_dict['storePrice'+str(count)]['storeID'] in storeArr):
        temp_dict['storePrice'+str(count)]['itemPrice'] = rows_id[tempStoreDict[2]][0]
        temp_dict['storePrice'+str(count)]['exists'] = True
    else:
        temp_dict['storePrice'+str(count)]['itemPrice'] = None
        temp_dict['storePrice'+str(count)]['exists'] = False

    count +=1

    temp_dict['storePrice'+str(count)] = {}
    temp_dict['storePrice'+str(count)]['storeID'] = defaultStoresArr[2]
    if(temp_dict['storePrice'+str(count)]['storeID'] in storeArr):
        temp_dict['storePrice'+str(count)]['itemPrice'] = rows_id[tempStoreDict[3]][0]
        temp_dict['storePrice'+str(count)]['exists'] = True
    else:
        temp_dict['storePrice'+str(count)]['itemPrice'] = None
        temp_dict['storePrice'+str(count)]['exists'] = False

    count +=1

    print(temp_dict)
    return temp_dict

    #else:
    #    print('No prices')
    #    return None

def query_getListNameByID(listID):
    query = 'SELECT listName FROM user_list WHERE uniqueID = ' + str(listID) + ';'
    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    return rows_id[0][0]

def treatBrand(testString):
    itemName = testString
    itemBrand = ''

    if '%|%' in testString:
        temp = testString.split('%|%',1)
        itemName = temp[0]
        itemBrand = temp[1]
        if(itemBrand[0] == ' '):
            itemBrand = itemBrand.replace(' ','')

    return itemName,itemBrand

def api_updateDefaultList(request):
    dict_data = json.loads(request.body.decode('utf-8'))
    userToken = request.COOKIES.get('token')
    userID = tokenToUser(userToken)
    listID = dict_data['listID']
    data = {}

    if(query_updateDefaultList(listID, userID)):
        data['status'] = 200
        data['message'] = 'Default list updated'
    else:
        data['status'] = 400
        data['message'] = 'Could not update default list'

    return JsonResponse(data)

def query_updateDefaultList(listID, userID):
    query = ''' UPDATE users_extended SET defaultList = ''' + str(listID) + ''' WHERE userID = ''' + str(userID) + ''';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(cursor_id.rowcount > 0):
        return True
    else:
        return False


########## FILL INFO ##########

def api_fillInfo(request):

    userToken = request.COOKIES.get('token')
    userID = tokenToUser(userToken)

    retDict = query_getInfoFill(userID)

    return JsonResponse(retDict)

def query_getInfoFill(userID):
    query = '''SELECT u.username, u.userMail, e.phoneNum FROM users u INNER JOIN users_extended e ON u.uniqueID = e.userID WHERE u.uniqueID = ''' + str(userID) +''';'''

    print(query)
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    userDict = {}
    userDict['userInfo'] = {}

    for i in rows_id:
        tempDict = {}
        tempDict['username'] = i[0]
        tempDict['userMail'] = i[1]
        tempDict['phoneNum'] = i[2]

    userDict['userInfo'] = tempDict


    return userDict

def api_getInfoForUsersInList(request):
    dict_data = json.loads(request.body.decode('utf-8'))
    listID = dict_data['listID']
    pendingUsers = query_getPendingUsers(listID)
    acceptedUsers = query_getAcceptedUsers(listID)
    data = { 'Accepted' : acceptedUsers , 'Pending' : pendingUsers }

    return JsonResponse(data)

def query_getPendingUsers(listID):

    query = ''' SELECT userID FROM list_invites WHERE listID = '''+str(listID)+''' AND invite_status = 'Pending';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    ret_dict = {}
    totalUsers = 0

    if(cursor_id.rowcount > 0):
        for i in rows_id:
            ret_dict['user'+str(totalUsers)] = {}
            temp_phone,temp_name = query_getUserPhoneAndName(i[0])
            ret_dict['user'+str(totalUsers)]['status'] = 'Pending'
            ret_dict['user'+str(totalUsers)]['userID'] = i[0]
            ret_dict['user'+str(totalUsers)]['userName'] = temp_name
            ret_dict['user'+str(totalUsers)]['phoneNum'] = temp_phone
            totalUsers += 1

        ret_dict['totalPendingUsers'] = totalUsers
        return ret_dict
    else:
        ret_dict['totalPendingUsers'] = 0
        return ret_dict

def query_getAcceptedUsers(listID):

    query = '''SELECT DISTINCT(li.userID) FROM list_invites li INNER JOIN user_list_participants ulp ON li.userID = ulp.userID AND ulp.listID = li.listID WHERE li.listID = '''+str(listID)+''' ;'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    ret_dict = {}
    totalUsers = 0

    if(cursor_id.rowcount > 0):
        for i in rows_id:
            ret_dict['user'+str(totalUsers)] = {}
            temp_phone,temp_name = query_getUserPhoneAndName(i[0])
            ret_dict['user'+str(totalUsers)]['status'] = 'Accepted';
            ret_dict['user'+str(totalUsers)]['userID'] = i[0]
            ret_dict['user'+str(totalUsers)]['userName'] = temp_name
            ret_dict['user'+str(totalUsers)]['phoneNum'] = temp_phone
            totalUsers += 1

        ret_dict['totalAcceptedUsers'] = totalUsers
        return ret_dict
    else:
        ret_dict['totalAcceptedUsers'] = 0
        return ret_dict

def query_getUserPhoneAndName(userID):

    query = ''' SELECT ue.phoneNum,u.username FROM users_extended ue INNER JOIN users u on ue.userID = u.uniqueID where ue.userID = ''' +str(userID)+''';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(cursor_id.rowcount > 0):
        return rows_id[0][0],rows_id[0][1]
    else:
        return None

########## SEND INVITES ##########

def api_getParticipant(request):

    dict_data = json.loads(request.body.decode('utf-8'))
    temp_phone = dict_data['phoneNum']
    listID = dict_data['listID']
    userToken = request.COOKIES.get('token')
    selfID = tokenToUser(userToken)
    data={}

    userID = query_getParticipant(temp_phone)

    if(selfID != userID):
        if(not userID):
            data['status'] = 300
            data['message'] = 'Phone number does not exist '

        elif(userID):
            data['status'] = 200
            data['message'] = 'User found'

            if(not query_checkIfAlreadyParticipant(userID,listID)):

                if(query_checkDupeInvite(userID,listID)):

                    if(query_addInvite(userID,listID)):
                        data['status'] = 200
                        data['message'] = 'Invite added'

                    else:
                        data['status'] = 400
                        data['message'] = 'Could not create invite'
                else:
                    data['status'] = 200
                    data['message'] = 'Invite already exists'

            else:
                data['status'] = 600
                data['message'] = 'User already in list as participant'
    else:
        data['status'] = 500
        data['message'] = 'Sending invite to self'

    return JsonResponse(data)

def query_checkDupeInvite(userID,listID):
    query = ''' SELECT EXISTS ( SELECT 1 userID FROM list_invites WHERE userID ='''+str(userID)+''' AND listID = '''+str(listID)+''' AND invite_status = 'Pending');'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    print(rows_id[0][0])

    if(rows_id[0][0] == 0):
        return True
    else:
        print('Invite already exists')
        return False

def query_checkIfAlreadyParticipant(userID,listID):
    query = ''' SELECT EXISTS ( SELECT 1 FROM user_list_participants WHERE userID ='''+str(userID)+''' AND listID = '''+str(listID)+''');'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    print(rows_id[0][0])

    if(rows_id[0][0] == 1):
        return True
    else:
        print('User already in list as participant')
        return False

def query_getParticipant(phoneNum):
    query = ''' SELECT IFNULL ( ( SELECT userID FROM users_extended WHERE phoneNum ='''+str(phoneNum)+''' ), 0);'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    print(rows_id[0][0])

    if(rows_id[0][0] != 0):
        return rows_id[0][0]
    else:
        print('Couldnt find user')
        return None

def query_addInvite(userID,listID):
    print('##############')
    print(userID)
    print(listID)
    print('##############')
    query = '''INSERT INTO list_invites VALUES(NULL,'''+str(listID)+''','''+str(userID)+''','Pending');'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)

    if(cursor_id.rowcount > 0):
        return True
    else:
        print('Couldnt add invite')
        return False

########## GET INVITES ##########

def api_getUserInvites(request):

    userToken = request.COOKIES.get('token')
    userID = tokenToUser(userToken)
    data = {}

    userInvites = query_checkUserInvites(userID)

    if(not userInvites):
        data['status'] = 400
        data['message'] = 'User does not have invites'

    else:
        temp_dict = {}
        totalInvites = 0
        for i in userInvites:
            listName = query_getListName(i)
            listOwner = query_getOwnerOfInvite(i)
            temp_dict['invite' + str(totalInvites)] = {}
            temp_dict['invite' + str(totalInvites)]['listID'] = i
            temp_dict['invite' + str(totalInvites)]['listName'] = listName
            temp_dict['invite' + str(totalInvites)]['listOwner'] = listOwner
            totalInvites +=1

        temp_dict['status'] = 200
        temp_dict['totalInvites'] = totalInvites
        data = temp_dict

    return JsonResponse(data)

def query_getOwnerOfInvite(listID):
    query = '''SELECT u.username FROM users u INNER JOIN user_list ul ON u.uniqueID = ul.ownerID WHERE ul.uniqueID = ''' + str(listID) + ''';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(cursor_id.rowcount > 0):
        return rows_id[0][0]
    else:
        print('No owner found')
        return None

def query_checkUserInvites(userID):
    query = '''SELECT listID from list_invites where userID = '''+str(userID)+''' AND invite_status = 'Pending';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    ret_arr = []

    if(cursor_id.rowcount > 0):

        temp_arr = []
        for i in rows_id:
            temp_arr.append(i[0])

        ret_arr = temp_arr

        return ret_arr
    else:
        print('No invites')
        return None

def query_getListName(listID):

    query = ''' SELECT listName FROM user_list WHERE uniqueID = ''' + str(listID) +''';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(cursor_id.rowcount > 0):
        return rows_id[0][0]

    else:
        print('Couldnt find list names')
        return None

########## REPLY TO INVITES ##########
def api_replyToUserInvites(request):

    dict_data = json.loads(request.body.decode('utf-8'))
    userToken = request.COOKIES.get('token')
    userID = tokenToUser(userToken)
    inviteReply = dict_data['reply']
    listID = dict_data['listID']
    data = {}

    # if user replies with Accept invite then a True is sent, if its refused then a False is sent
    if(inviteReply):

        if(query_updateParticipants(userID,listID)):
            if(query_updateStatus(True,userID,listID)):
                data['status'] = 200
                data['message'] = 'Invite status now accepted'
            else:
                data['status'] = 400
                data['message'] = 'Could not update status'

        else:
            data['status'] = 400
            data['message'] = 'Could not add new participant'

    elif(not inviteReply):

        if(query_updateStatus(False,userID,listID)):
            data['status'] = 200
            data['message'] = 'Invite status now refused'
        else:
            data['status'] = 400
            data['message'] = 'Could not update status'
    else:
        data['status'] = 400
        data['message'] = 'Server error'

    return JsonResponse(data)

def query_updateParticipants(userID,listID):
    query = ''' INSERT INTO user_list_participants VALUES(NULL,'''+str(listID)+''','''+str(userID)+''',2);'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)

    if(cursor_id.rowcount > 0):
        return True
    else:
        print('Couldnt add new participant')
        return False

def query_updateStatus(bool,userID,listID):

    if(bool):
        newStatus = 'Accepted'
    else:
        newStatus = 'Refused'

    query = ''' UPDATE list_invites SET invite_status = "''' + newStatus + '''" WHERE userID = ''' + str(userID) +''' AND listID = ''' + str(listID)+''';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)

    if(cursor_id.rowcount > 0):
        return True
    else:
        print('Couldnt update status')
        return False
