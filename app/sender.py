from .extensions import mongo

import requests,json,time

    


def get_access_token(client_id,client_secret,isprod):
    #  getting the access-token for sending the data
    if isprod:
        url = "https://partners.cloudkitchens.com/v1/auth/token"
    else:

        url = "https://partners-staging.cloudkitchens.com/v1/auth/token"

    payload='grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret+'&scope=ping%20orders.create%20orders.status_update'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    resp = json.loads(response.text)
    
    
    return resp['access_token']



def send_data(raw_data_delivered,restaurant_id,partner_id):
    
    
    # this is the partner config collection conating details of the configuration of the partner while sending the information
    partner_conf = mongo.db.partner_conf
    # we fetch the access-token from database for auth while sending the data to CK
    partner_con = partner_conf.find_one({'partner_id':partner_id})
    if partner_con['is_prod']:

        client_id , client_secret ,access_token= partner_con['client_id_prod'],partner_con['client_secret_prod'],partner_con['api_key_prod'] 
        # access_token = get_access_token()
        
        # using the access token for sending the data
        url = "https://partners.cloudkitchens.com/v1/orders"
    else:
        client_id , client_secret ,access_token= partner_con['client_id_dev'],partner_con['client_secret_dev'],partner_con['api_key_dev'] 
        # access_token = get_access_token()
        
        # using the access token for sending the data
        url = "https://partners-staging.cloudkitchens.com/v1/orders"
    
    headers = {
    'X-Application-Id': client_id,
    'X-Store-Id': str(restaurant_id),
    'Authorization': 'Bearer '+access_token,
    'Content-Type': 'application/json'
    }
   
    
    for ind,i in enumerate([0,1,1,2,3,5,8]):
        time.sleep(i)
        
        response = requests.request("POST", url, headers=headers, data=raw_data_delivered.encode('utf-8'))
        
        if response.status_code==200:
            break
        if response.status_code==401:
            access_token = get_access_token(client_id,client_secret,partner_con['is_prod'])
            headers['Authorization']='Bearer '+access_token
            query_params = { "partner_id":partner_id }
            if partner_con['is_prod']:
                new_token = { "$set": { "api_key_prod": access_token } }
            else:
                new_token = { "$set": { "api_key_dev": access_token } }
            partner_conf.update_one(query_params, new_token)
        if i==8:
            
            return False,ind,response.status_code,response.text
    return True,ind,response.status_code,response.text
    # return True



def cancel_postorder(order_id,restaurant_id,partner_id):
    
    
    # this is the partner config collection conating details of the configuration of the partner while sending the information
    partner_conf = mongo.db.partner_conf
    # we fetch the access-token from database for auth while sending the data to CK
    partner_con = partner_conf.find_one({'partner_id':partner_id})
    if partner_con['is_prod']:

        client_id , client_secret ,access_token= partner_con['client_id_prod'],partner_con['client_secret_prod'],partner_con['api_key_prod'] 
        # access_token = get_access_token()
        
        # using the access token for sending the data
        url = "https://partners.cloudkitchens.com/v1/orders/"+str(order_id)+"/status"
    else:
        client_id , client_secret ,access_token= partner_con['client_id_dev'],partner_con['client_secret_dev'],partner_con['api_key_dev'] 
        # access_token = get_access_token()
        
        # using the access token for sending the data
        url ="https://partners-staging.cloudkitchens.com/v1/orders/"+str(order_id)+"/status"
     


    

    payload={"orderStatus":"CANCELED"}
    payload = json.dumps(payload)


    headers = {
    'X-Application-Id': client_id,
    'X-Store-Id': str(restaurant_id),
    'Authorization': 'Bearer '+access_token,
    'Content-Type': 'application/json',
    'Cookie': '__cfduid=dc08d96dd9c092e206d25e729363ab2371608203519'
    }

    for ind,i in enumerate([0,1,1,2,3,5,8]):
        time.sleep(i)
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        if response.status_code==202:
            break
        if response.status_code==401:
            access_token = get_access_token(client_id,client_secret,partner_con['is_prod'])
            headers['Authorization']='Bearer '+access_token
            query_params = { "partner_id":partner_id }
            if partner_con['is_prod']:
                new_token = { "$set": { "api_key_prod": access_token } }
            else:
                new_token = { "$set": { "api_key_dev": access_token } }
            partner_conf.update_one(query_params, new_token)
        if i==8:
            
            return False,ind,response.status_code,response.text
    return True,ind,response.status_code,response.text

def update_postorder(order_id,restaurant_id,order_status,partner_id):
    # this is the partner config collection conating details of the configuration of the partner while sending the information
    partner_conf = mongo.db.partner_conf
    # we fetch the access-token from database for auth while sending the data to CK
    partner_con = partner_conf.find_one({'partner_id':partner_id})
    if partner_con['is_prod']:
    
        client_id , client_secret ,access_token= partner_con['client_id_prod'],partner_con['client_secret_prod'],partner_con['api_key_prod'] 
        # access_token = get_access_token()
        
        # using the access token for sending the data
        url = "https://partners.cloudkitchens.com/v1/orders/"+str(order_id)+"/status"
    else:
        client_id , client_secret ,access_token= partner_con['client_id_dev'],partner_con['client_secret_dev'],partner_con['api_key_dev'] 
        # access_token = get_access_token()
        
        # using the access token for sending the data
        url ="https://partners-staging.cloudkitchens.com/v1/orders/"+str(order_id)+"/status"

    payload={"orderStatus":order_status}
    payload = json.dumps(payload)


    headers = {
    'X-Application-Id': client_id,
    'X-Store-Id': str(restaurant_id),
    'Authorization': 'Bearer '+access_token,
    'Content-Type': 'application/json',
    'Cookie': '__cfduid=dc08d96dd9c092e206d25e729363ab2371608203519'
    }

    for ind,i in enumerate([0,1,1,2,3,5,8]):
        time.sleep(i)
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        if response.status_code==202:
            break
        if response.status_code==401:
            access_token = get_access_token(client_id,client_secret,partner_con['is_prod'])
            headers['Authorization']='Bearer '+access_token
            query_params = { "partner_id":partner_id }
            if partner_con['is_prod']:
                new_token = { "$set": { "api_key_prod": access_token } }
            else:
                new_token = { "$set": { "api_key_dev": access_token } }
            partner_conf.update_one(query_params, new_token)
        if i==8:
            
            return False,ind,response.status_code,response.text
    return True,ind,response.status_code,response.text

