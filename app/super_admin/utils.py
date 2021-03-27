import uuid
length_pid = 4
import requests
from flask import json,url_for
from ..extensions import mongo
from .auth import auth_goomer
import datetime
from datetime import timezone
import numpy as np
from collections import OrderedDict
import pandas as pd
import warnings
from ..settings.settings import GOOMER_WEBHOOK_REGISTER_URL
warnings.filterwarnings("ignore")
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

def generate_partner_id(name):
    if len(name)>2:
        first_letters = name[:3]
        rest = length_pid
    else:
        first_letters = name
        rest = 3+length_pid-len(name)
        
    id = uuid.uuid4()
    
    
    rest_id = str(id.int)[:rest]
    
    partner_id = first_letters+rest_id
    
    partner_collection = mongo.db.partners
    
    partner = partner_collection.find({'partner_id':partner_id})
    if not partner:
        partner_id = generate_partner_id(name)
    return partner_id
    


length_uid = 9
def generate_user_id():
    id = uuid.uuid4()
    
    
    user_id = str(id.int)[:length_uid]
    
    
    
    user_collection = mongo.db.users
    
    user = user_collection.find({'user_id':user_id})
    if not user:
        user_id = generate_user_id()
    return user_id


def dashboard_chart(orders):
    df = pd.DataFrame(orders)
    

    df['last_seen'] = pd.to_datetime(df['last_seen'])


    created_outgoing = df[df['order_state']==1][df['response_code']==200].groupby([df['last_seen'].dt.strftime('%y/%m/%d')]).count()['_id'].to_dict()
    created_incoming = df[df['order_state']==1].groupby([df['last_seen'].dt.strftime('%y/%m/%d')]).count()['_id'].to_dict()
    cancelled_outgoing = df[df['order_state']==2][df['response_code']==202].groupby([df['last_seen'].dt.strftime('%y/%m/%d')]).count()['_id'].to_dict()
    cancelled_incoming = df[df['order_state']==2].groupby([df['last_seen'].dt.strftime('%y/%m/%d')]).count()['_id'].to_dict()
    
    if created_outgoing.keys()!=created_incoming.keys() or cancelled_outgoing.keys()!=cancelled_incoming.keys() or cancelled_outgoing!=created_outgoing :
   
        all_dates = list(np.unique(list(created_outgoing.keys())+list(created_incoming.keys())+list(cancelled_outgoing.keys())+list(cancelled_incoming.keys()) ))
        
        for dates in all_dates:
            
            if dates not in created_outgoing.keys():
                created_outgoing[dates] = 0
            if dates not in created_incoming.keys():
                created_incoming[dates] = 0
            if dates not in cancelled_outgoing.keys():
                cancelled_outgoing[dates] = 0
            if dates not in cancelled_incoming.keys():
                cancelled_incoming[dates] = 0

        created_outgoing ={datetime.datetime.strptime(item[0], "%y/%m/%d").strftime('%d/%m/%y'):item[1] for item in sorted(created_outgoing.items(), key=lambda val: val[0])}
        created_incoming ={datetime.datetime.strptime(item[0], "%y/%m/%d").strftime('%d/%m/%y'):item[1] for item in sorted(created_incoming.items(), key=lambda val: val[0])}
        cancelled_outgoing ={datetime.datetime.strptime(item[0], "%y/%m/%d").strftime('%d/%m/%y'):item[1] for item in sorted(cancelled_outgoing.items(), key=lambda val: val[0])}
        cancelled_incoming ={datetime.datetime.strptime(item[0], "%y/%m/%d").strftime('%d/%m/%y'):item[1] for item in sorted(cancelled_incoming.items(), key=lambda val: val[0])}

        


    cancelled_pie = df[df['order_state']==2].groupby([df[df['response_code']!=202]['response_code']]).count()['_id'].to_dict()

    created_pie = df[df['order_state']==1].groupby([df[df['response_code']!=200]['response_code']]).count()['_id'].to_dict()

    chart_created_orders= {'dates':list(created_outgoing.keys()),'incoming':list(created_incoming.values()),'outgoing':list(created_outgoing.values()),'pie_labels':list(created_pie.keys()),'pie_values':list(created_pie.values())}
    
    chart_cancelled_orders = {'dates':list(cancelled_outgoing.keys()),'incoming':list(cancelled_incoming.values()),'outgoing':list(cancelled_outgoing.values()),'pie_labels':list(cancelled_pie.keys()),'pie_values':list(cancelled_pie.values())}

    created_array = df[df['order_state']==1][df['response_code']!=200][['partner_id','store_id_by_ck','error_message','response_code','last_seen','order_id']].to_numpy()
    cancelled_array = df[df['order_state']==2][df['response_code']!=202][['partner_id','store_id_by_ck','error_message','response_code','last_seen','order_id']].to_numpy()
    
    
    return chart_created_orders,chart_cancelled_orders,created_array,cancelled_array