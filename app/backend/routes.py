from flask import Blueprint ,request,jsonify

import datetime
from datetime import timezone
from passlib.hash import pbkdf2_sha256
from .utils import generate_user_id,generate_admin_key
from functools import wraps
from ..extensions import mongo
from pandas import DataFrame

# the blueprint name for the routes accessed by dashboard user is dboard
backend = Blueprint('backend', __name__, url_prefix='/backend')

def verify_key(f):
    # this is the decorator for verifying the api-key
    @wraps(f)
    def decorated(*args, **kwargs):
    

        if 'x-api-key' in request.headers:
            key = request.headers['x-api-key']
            # user_collection = mongo.db.users
            
            # user = user_collection.find_one({'super_admin_key':key})
            if key=='63abd98e-7b9d-443d-acdb-8c1373f2c8f2':         
                    return f(*args, **kwargs)
            # no key matches
            return jsonify({"Error":"Invalid Api key"})
        else:
            # no key provided
            return jsonify({"Error":"No api key provided"})
 
    return decorated

# @backend.route('/add_user',methods=["POST"])
# @verify_key
# def add_user():
    
#     user_collection = mongo.db.users
    
#     email_id = request.form.get('email')
#     user_already = user_collection.find_one({'email_id':email_id})
#     if user_already:
#         return {"Error":"User already present"}
#     user_id = generate_user_id()
#     first_name = request.form.get('first_name')
#     last_name = request.form.get('last_name')
#     password = request.form.get('password')
#     created_on = datetime.datetime.now(tz=timezone.utc)
#     user_permissions = request.form.get('permission_id')
#     is_active = False
#     last_updated_on = created_on
    
#     new_user = {'user_id':user_id,
#     'first_name':first_name,
#     'last_name':last_name,
#     'email_id':email_id,
#     'password':pbkdf2_sha256.encrypt(password),
#     'created_on':created_on,
#     'user_permissions':user_permissions,
#     'last_updated_on':last_updated_on,
#     'is_active':is_active}
#     return_val = {'success':1}
#     if user_permissions==1:
#         admin_key = generate_admin_key()
#         new_user['admin_key']=admin_key
#         return_val['x-api-key'] = admin_key
#     user_collection.insert(new_user)

#     return return_val

import datetime as dt


@backend.route('/transformer_logs',methods=["POST"])
@verify_key
def transformer_logs():
    # print(request.form)
    data_transformer = mongo.db.data_transformer
    restaurant_collection = mongo.db.restaurants
    partners_collection = mongo.db.partners


    start_date = request.form['start_date']
    end_date = request.form['end_date']
    platform_name = request.form['platform_name']

    start_date = dt.datetime.strptime(start_date.strip(),'%Y-%m-%d')
    end_date = dt.datetime.strptime(end_date.strip(),'%Y-%m-%d') + dt.timedelta(days=1)

    partner= partners_collection.find_one({'partner_name':platform_name})
    if not partner:
        return {'error':'invalid platform name'}
    partner_id = partner['partner_id']
    orders = data_transformer.find({"last_seen":{'$gte':start_date, '$lt':end_date },'partner_id':partner_id})
    
    lis_log =[]
    for v in orders:
        logs ={}
        
        logs['partner_id'] = v['partner_id']
        logs['order_id'] = v['order_id']
        logs['restaurant_id'] = v['store_id_by_ck']
        if 'restaurant_id' in v:

            logs['internal_restaurant_id'] = v['restaurant_id']
        logs['error_message'] = v['error_message']
        if 'trial_times' in v:

            logs['trial_times'] = v['trial_times']
        
        logs['last_seen'] = v['last_seen']
        logs['order_state']=v['order_state']
        if 'response_code' in v:
            logs['resp_code']=v['response_code']
        if 'order_accept_resp_code' in v:

            logs['order_accept_resp_code']=v['order_accept_resp_code']
        
        lis_log.append(logs)
    return {'logs':lis_log},200

@backend.route('/transformer_logs/<order_id>')
@verify_key
def transformer_logs_based_on_order_id(order_id):
    data_transformer = mongo.db.data_transformer
    
    orders = data_transformer.find({'order_id':order_id})
    
    lis_log =[]
    for v in orders:
        logs ={}
        
        logs['partner_id'] = v['partner_id']
        logs['order_id'] = v['order_id']
        logs['restaurant_id'] = v['store_id_by_ck']
        if 'restaurant_id' in v:

            logs['internal_restaurant_id'] = v['restaurant_id']
        logs['error_message'] = v['error_message']
        if 'trial_times' in v:

            logs['trial_times'] = v['trial_times']
        
        logs['last_seen'] = v['last_seen']
        logs['order_state']=v['order_state']
        if 'response_code' in v:
            logs['resp_code']=v['response_code']
        if 'order_accept_resp_code' in v:

            logs['order_accept_resp_code']=v['order_accept_resp_code']
        
        lis_log.append(logs)
    if len(lis_log)==0:
        
        orders = data_transformer.find({'order_id':int(order_id)})
        for v in orders:
            logs ={}
        
            logs['partner_id'] = v['partner_id']
            logs['order_id'] = v['order_id']
            logs['restaurant_id'] = v['store_id_by_ck']
            if 'restaurant_id' in v:

                logs['internal_restaurant_id'] = v['restaurant_id']
            logs['error_message'] = v['error_message']
            if 'trial_times' in v:

                logs['trial_times'] = v['trial_times']
            
            logs['last_seen'] = v['last_seen']
            logs['order_state']=v['order_state']
            if 'response_code' in v:
                logs['resp_code']=v['response_code']
            if 'order_accept_resp_code' in v:

                logs['order_accept_resp_code']=v['order_accept_resp_code']
            
            lis_log.append(logs)

    return {'logs':lis_log},200



@backend.route('/logs/<platform_name>',methods=["GET"])
def transformer_logs_browser(platform_name):
    # print(request.form)
    data_transformer = mongo.db.data_transformer
    restaurant_collection = mongo.db.restaurants
    partners_collection = mongo.db.partners


    start_date = dt.datetime.now(tz=timezone.utc) - dt.timedelta(days=1)
    end_date = dt.datetime.now(tz=timezone.utc)
    

    

    partner= partners_collection.find_one({'partner_name':platform_name})
    if not partner:
        return {'error':'invalid platform name'}
    partner_id = partner['partner_id']
    orders = data_transformer.find({"last_seen":{'$gte':start_date, '$lt':end_date },'partner_id':partner_id})
    
    lis_log =[]
    for v in orders:
        logs ={}
        
        logs['partner_id'] = v['partner_id']
        logs['order_id'] = v['order_id']
        logs['restaurant_id'] = v['store_id_by_ck']
        if 'restaurant_id' in v:

            logs['internal_restaurant_id'] = v['restaurant_id']
        else:
            logs['internal_restaurant_id'] = None
        logs['error_message'] = v['error_message']
        if 'trial_times' in v:

            logs['trial_times'] = v['trial_times']
        else:
            logs['trial_times'] = None
        logs['last_seen'] = v['last_seen']
        logs['order_state']=v['order_state']
        if 'response_code' in v:
            logs['resp_code']=v['response_code']
        else:
            logs['resp_code']= None
        if 'order_accept_resp_code' in v:

            logs['order_accept_resp_code']=v['order_accept_resp_code']
        else:
            logs['order_accept_resp_code']= None
        if 'order_status_mapping' in v:
            logs['order_status_mapping'] = v['order_status_mapping']
        else:
            logs['order_status_mapping'] = None
        lis_log.append(logs)
    df = DataFrame(lis_log[::-1]).to_html()
    return df
