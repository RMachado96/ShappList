from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.db import connection, transaction
import json

def api_getProducts(request):

    dict_data = json.loads(request.body.decode('utf-8'))
    searchbar_keyword = dict_data['searchbar_keyword']
    category = dict_data['category']
    sub_category = dict_data['sub_category']
    product_dict = {}
    product_dict['searchbar_keyword'] = dict_data['searchbar_keyword']
    product_dict['category'] = dict_data['category']
    product_dict['sub_category'] = dict_data['sub_category']
    product_dict['orderBy'] = dict_data['orderBy']
    product_dict['clause'] = dict_data['clause']

    query = select_query(product_dict)

    data = executeQuery(query)

    return JsonResponse(data)

def api_getProductsWithDiscount(request):
    query = ''' SELECT uniqueID,itemName,itemPrice,priceType,itemCategory,itemSubCategory,imgPath,discountValue,storeID from products where discountValue != 1;'''

    data = executeQuery(query)

    return JsonResponse(data)

def api_getProductLowestPrice(request):
    # executar no ultimo botao "Adicionar produto", antes de adicionar o produto à lista // repetir a toda a lista sempre que regras sejam alteradas
    # receber ID --> encontrar nome pelo ID --> procurar todos pelo mesmo nomes --> return produto com o menor preço baseado nas lojas permitidas
    dict_data = json.loads(request.body.decode('utf-8'))
    baseProductID = dict_data['baseProductID']
    #allowedStores = create api in listService to get allowed stores listID = dict_data['listID']

    itemName = query_getItemNameByID(baseProductID)
    listIDs, listPrices, listStores = query_getAllIDsByName(itemName)
    bestID = support_getLowestPrice(listPrices, listIDs,listStores)

    data = {'bestID' : bestID}

    return JsonResponse(data)

def query_getItemNameByID(productID):
    query = '''SELECT itemName FROM products WHERE uniqueID='''+str(productID)+''';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    if(cursor_id.rowcount > 0):
        result = rows_id[0][0]
        return result
    else:
        print('Couldnt find product')

def query_getAllIDsByName(itemName):
    query = ''' SELECT uniqueID,itemPrice,storeID FROM products WHERE itemName= \''''+ itemName +'''\';'''
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()
    listIDs = []
    listPrices = []
    listStores = []

    if(cursor_id.rowcount > 0):
        for i in rows_id:
            listIDs.append(i[0])
            listPrices.append(i[1])
            listStores.append(i[2])

        return listIDs,listPrices,listStores
    else:
        print('Couldnt find product')

def support_getLowestPrice(listPrices,listIDs,listStores):
    lowest = 9999;
    bestID = 0;
    #for test
    allowedStores = [1,2,3]
    for i in range(len(listStores) - 1 ):
        if(listStores[i] in allowedStores):
            if(listPrices[i]<lowest):
                lowest = listPrices[i]
                bestID = listIDs[i]

    return bestID

def select_query(product_dict):
    query = 'SELECT uniqueID,itemName,itemPrice,priceType,itemCategory,itemSubCategory,imgPath,discountValue,storeID FROM products WHERE '
    boolSearch = False
    boolCategory = False

    if(product_dict['searchbar_keyword'] != ''):
        sub_stringSearch = 'itemName like \'%' + product_dict['searchbar_keyword'] + '%\''
        boolSearch = True

    if(product_dict['sub_category'] != ''):
        sub_stringCategory = 'itemSubCategory = \'' + product_dict['sub_category'] + '\''
        boolCategory = True

    elif(product_dict['category'] != ''):
        sub_stringCategory = 'itemCategory = \'' + product_dict['category'] + '\''
        boolCategory = True
    elif(product_dict['searchbar_keyword'] == ''):
        sub_stringSearch = 'itemName like \'%%\''
        boolSearch = True


    if(boolSearch and boolCategory):
        finalQuery = query + sub_stringSearch + ' AND ' + sub_stringCategory
    elif(boolSearch):
        finalQuery = query + sub_stringSearch
    elif(boolCategory):
        finalQuery = query + sub_stringCategory

    finalQuery = finalQuery + 'ORDER BY '+product_dict['orderBy']+' '+ product_dict['clause']+ ';'
    print(finalQuery)
    return finalQuery

def executeQuery(query):
    print('EXECUTE QUERY HERE')
    cursor_id = connection.cursor()
    cursor_id.execute(query)
    rows_id = cursor_id.fetchall()

    query_resultSize = len(rows_id)
    data = {}
    data['totalSize'] = len(rows_id)
    data['products'] = {}
    found_products = {}
    total_products = 0
    lastAdded = 0
    for i in range(query_resultSize):
        temp_dict = {}

        if rows_id[i][1] not in found_products.values():


            temp_dict['id'] = []
            temp_dict['storeID'] = []
            temp_dict['preco'] = []
            temp_dict['desconto'] = []

            temp_dict['id'].append(rows_id[i][0])
            temp_dict['nome'], temp_dict['marca'] = treatBrand(rows_id[i][1])
            temp_dict['preco'].append(rows_id[i][2])
            temp_dict['tipo_preco'] = rows_id[i][3]
            temp_dict['categoria'] = rows_id[i][4]
            temp_dict['sub_categoria'] = rows_id[i][5]
            temp_dict['path'] = rows_id[i][6]
            temp_dict['desconto'].append(rows_id[i][7])
            temp_dict['storeID'].append(rows_id[i][8])

            data['products']['prod' + str(lastAdded)] = temp_dict
            found_products['prod' + str(lastAdded)] = rows_id[i][1]
            lastAdded +=1
            total_products +=1
            #print(found_products)
        else:
            temp_nome,temp_marca = treatBrand(rows_id[i][1])
            existent_key = getKeyByValue(data,temp_nome,temp_marca)
            data['products'][existent_key]['id'].append(rows_id[i][0])
            data['products'][existent_key]['preco'].append(rows_id[i][2])
            data['products'][existent_key]['desconto'].append(rows_id[i][7])
            data['products'][existent_key]['storeID'].append(rows_id[i][8])

    data['totalSize'] = total_products
    return data

def getKeyByValue(data,value,brand):
    totalDictSize = len(data['products'])
    #print('size of dict is : ' + str(totalDictSize))
    #print(data)
    if(totalDictSize == 1):
        #print('im here2')
        if data['products']['prod' + str(0)]['nome'] == value and data['products']['prod' + str(0)]['marca'] == brand:
            #print('returning')
            return 'prod' + str(0)
    else:
        #print('starting for')
        for i in range(totalDictSize):
            #print('im here')
            #print(value)
            #print(brand)
            #print('prod' + str(i))

            if data['products']['prod' + str(i)]['nome'] == value and data['products']['prod' + str(i)]['marca'] == brand:
                #print('returning for')
                return 'prod' + str(i)

    #print(data)
    #print(value)
    #print(brand)
    return 'Error'

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

