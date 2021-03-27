import uuid
import requests
from flask import json,url_for
from ..extensions import mongo
from .auth import auth_goomer
from datetime import timezone
import datetime
from ..settings.settings import GOOMER_WEBHOOK_REGISTER_URL
length_rid = 5


        
def generate_restaurant_id(name):
    if len(name)>2:
        first_letters = name[:3]
        rest = length_rid
    else:
        first_letters = name
        rest = 3+length_rid-len(name)
        
    id = uuid.uuid4()
    
    
    rest_id = str(id.int)[:rest]
    
    restaurant_id = first_letters+rest_id
    
    restaurant_collection = mongo.db.restaurants
    
    restaurant = restaurant_collection.find({'restaurant_id':restaurant_id})
    if not restaurant:
        restaurant_id = generate_restaurant_id(name)
    return restaurant_id



def register_goomer_webhook(res_config,store_id):
    restaurant_config = mongo.db.restaurant_config
    
    token_dict = json.loads(auth_goomer(res_config,store_id))
    query = res_config
    
    new_val = token_dict
    
    
    new_val['token_updated_at'] = datetime.datetime.now(tz=timezone.utc)
    restaurant_config.update_one(query,{'$set':new_val})
    
    
    # this part is for registering webhook to goomer just add the webhook link here
    
    url = GOOMER_WEBHOOK_REGISTER_URL

    payload={"orderReceived": url_for('Goomer.new_order',_external=True),"orderCanceled":url_for('Goomer.cancel_order',_external=True) ,'orderUpdated':url_for('Goomer.update_order',_external=True) }
    # print(payload)
    payload = json.dumps(payload)
    headers = {
            'x-api-key': new_val['authToken'],
            'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    return response.status_code==200


def add_justo_res(res_query):
    restaurant_collection = mongo.db.restaurants
    
    restaurant_collection.insert_one(res_query)
    


def add_config_res(res_query,res_config):
    restaurant_collection = mongo.db.restaurants
    restaurant_config = mongo.db.restaurant_config
    
    restaurant_collection.insert_one(res_query)
    
    restaurant_config.insert_one(res_config)
    res_config['store_id'] = res_query['partner_store_id']
    
    register_goomer_webhook(res_config)


def get_last_easi_order(res_obj):
    url = "https://test8.melbdelivery.com/open_api/v1/orders/latest" 
    headers = {}
    headers['secretKey'] = res_obj['secretKey']
    headers['accessKey'] = res_obj['accessKey']
    payload="{\r\n    \"page\": 1\r\n}"

    resp = requests.get(url,headers=headers,payload=payload)

    lis_order = json.loads(resp.text)
    order_id = 0
    if len(lis_order['data']):
        order_id = lis_order['data'][0]['order_info']['id']
    return order_id