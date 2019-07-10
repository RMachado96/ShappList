import requests
import json
import io

def verify_token(token):
    print('token received:')
    print(token)
    url = 'https://shapplist.pythonanywhere.com/api_verifytoken'
    data = {'token' : token}
    json_data = json.dumps(data)
    print('requesting something idfk')

    r = requests.post(url = url ,data = json_data)
  
    print('request done ')
   
   
    print(r.text)
    results = json.loads(r.text)
    print(results)
    
    print(type(results))

    if(results['boolean'] == 'True'):
        print('returning true')
        return True
    else:
        print('returning false')
        return False

