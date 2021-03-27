from functools import wraps

import requests
from flask import json
from ..settings.settings import GOOMER_AUTH_URL


def auth_goomer(res_config,store_id):
    
    

    url = GOOMER_AUTH_URL

    payload={"integrationToken": res_config['integration_token'],"storeId": store_id,"clientSecret": res_config['client_secret'],"clientId": res_config['client_id']}
    payload = json.dumps(payload)
    
    headers = {
    'x-api-key': res_config['restaurant_api_key'],
    'Authorization': 'Bearer '+str(res_config['restaurant_api_key']),
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    
    

    return(response.text)
