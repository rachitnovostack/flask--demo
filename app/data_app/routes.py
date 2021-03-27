from flask import Flask, jsonify, render_template, session, request
from flask import redirect, url_for
from flask import Blueprint,request ,json
import os
from functools import wraps
from ..extensions import mongo

data_ = Blueprint('Datalink', __name__, url_prefix='/data-link')

# @app.route('/')
# def index():
#     mongo_c = mongo.db.data_link
#     lis = mongo_c.find_one()
    
#     return {'succ':str(lis)}

def verify_key(f):
    # this is the decorator for verifying the api-key
    @wraps(f)
    def decorated(*args, **kwargs):

        if 'x-api-key' in request.headers:
            key = request.headers['x-api-key']
            verify = mongo.db.data_link.find_one({'x-api-key': key})
            # "keys" are the api keys available
            if verify:

                return f(*args, **kwargs)
            # no key matches
            return jsonify({"Error": "Invalid Api key"})
        else:
            # no key provided
            return jsonify({"Error": "No api key provided"})

    return decorated


@verify_key
@data_.route('/easi', methods=["POST"])
def data_link():
    restaurant_collection = mongo.db.restaurants
    res_config_collection = mongo.db.restaurant_config
    if 'partner_id' in dict(request.form).keys():
        if request.form['partner_id']=='EAS6969':

            lis_res = restaurant_collection.find({'partner_id': request.form['partner_id']})
            res_list = []
            for i in lis_res:
                
                res_config = res_config_collection.find_one({'restaurant_id':i['restaurant_id']})
                
                res_obj = {}
                res_obj['restaurant_name'] = i['restaurant_name']
                res_obj['restaurant_id'] = i['restaurant_id']
                res_obj['accessKey'] = res_config['accessKey']
                res_obj['secretKey'] = res_config['secretKey']
                res_obj['_id'] = str(res_config['_id'])
                res_obj['last_order_id'] = res_config['last_order_id']
                res_list.append(res_obj)
            return {'lis_res': res_list}
    
    return {'error':'enter valid partner id'}
        
