from flask import Blueprint ,request,session

from .utils import generate_restaurant_id,add_justo_res,register_goomer_webhook , get_last_easi_order

import datetime
import datetime as dt
from datetime import timezone
from ..extensions import mongo
from ..settings.settings import GOOMER_INTEGRATION_TOKEN
from flask import render_template,url_for,redirect
# the blueprint name for the routes accessed by sales user is sales
sales = Blueprint('sales', __name__, url_prefix='/sales')


#Here are the list of routes that sales user can use

@sales.route('/index',methods=["GET"])
def index():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))
    
    user = mongo.db.users.find_one({'user_id':session['user_id']})
    
    if not user:
        return redirect(url_for('login_page'))
    restaurant_collection = mongo.db.restaurants
    partner_collection = mongo.db.partners
    lis_partner = partner_collection.find()
    d={}
    for each_partner in lis_partner:
        d[each_partner['partner_id']] = each_partner['partner_name']

    
    user_details = {'first_name':user['first_name'],
                    'last_name':user['last_name'],
                    'email':user['email_id'],
                    'designation':'Sales'
                    }

    
    query = {'onboarded_by':session['user_id']}
    list_of_res = restaurant_collection.find(query)
    passed_lis = []
    for res in list_of_res:
        res_obj = {
            'restaurant_id':res['restaurant_id'],
            'store_id_by_ck':res['store_id_by_ck'],
            'restaurant_name':res['restaurant_name'],
            'res_webhook_url':url_for('Justo.new_order_webhook',_external=True),
            'restaurant_currency':res['restaurant_currency'],
            'restaurant_country':res['restaurant_country'],
            'res_partners':d[res['partner_id']]
        }
        if res['partner_id']=="Goo2290":
            res_obj['res_webhook_url']=url_for('Goomer.new_order',_external=True)
        passed_lis.append(res_obj)
    
    return render_template('sales/index.html',list_res=passed_lis[::-1],user_details=user_details,signout_url = url_for('login_page'))



@sales.route('/add_restaurant',methods=['POST'])
def add_restaurant():
    if 'logged_in' not in session:
        return redirect(url_for('/'))
    user = mongo.db.users.find_one({'user_id':session['user_id']})
    # this route is used to onboard a restaurant
    restaurant_collection = mongo.db.restaurants
    partners_collection = mongo.db.partners
    form_data = request.form

    # find the partner using 
    partner_details = partners_collection.find_one({'partner_name':form_data['restaurant_partner']})
    
    # the following four fields are taken as input by the admin user
    partner_id = partner_details['partner_id']
        
    restaurant_name = request.form.get('restaurant_name')
    
    store_id_by_ck= request.form.get('store_id_by_ck')

    restaurant_country = form_data['restaurant_country']

    restaurant_currency = form_data['restaurant_currency']
    
    res_obj = restaurant_collection.find_one({'store_id_by_ck':store_id_by_ck})   
    if res_obj:
        print('Error') 
        return redirect(url_for('sales.index'))
    
    # we generate a unique restaurant_id for a given restaurant name (restaurant_id is alpha-numeric key)
    restaurant_id = generate_restaurant_id(restaurant_name)
    
    # # current time of onboarding the restaurant is recorded
    onboarded_on = dt.datetime.now(tz=timezone.utc)
    # # currently the restaurant is active , it can be changed in future
    restaurant_is_active = True
    
    onboarded_by = user['user_id']
    # new_restaurant = {'restaurant_id':restaurant_id,'restaurant_name':restaurant_name,'partner_store_id':partner_store_id,'restaurant_contact':restaurant_contact,'restaurant_partner_id':restaurant_partner_id,'onboarded_by':onboarded_by,'onboarded_on':onboarded_on,'is_active':restaurant_is_active}
    try:
        new_restaurant = {'restaurant_id':restaurant_id,
        'restaurant_name':restaurant_name,
        'partner_id':partner_id,
        'store_id_by_ck':store_id_by_ck,
        'onboarded_on':onboarded_on,
        'is_active':restaurant_is_active,
        'restaurant_currency':restaurant_currency,
        'restaurant_country':restaurant_country,
        'onboarded_by':onboarded_by,
        'last_updated_by':onboarded_by,
        'last_updated_on':onboarded_on}
        if partner_id =='Jus2805':

            restaurant_collection.insert(new_restaurant)
        if partner_id=='Goo2290':
            restaurant_config = {
                'restaurant_id':restaurant_id,
                'integration_token':GOOMER_INTEGRATION_TOKEN,
                'restaurant_api_key':GOOMER_INTEGRATION_TOKEN,
                'client_id':request.form['client_id'],
                'client_secret':request.form['client_secret']
            }
            
            restaurant_config_collection = mongo.db.restaurant_config
            restaurant_config_collection.insert(restaurant_config)
            status = register_goomer_webhook(restaurant_config,store_id_by_ck)
            restaurant_collection.insert(new_restaurant)
        elif partner_id=='EAS6969':
            restaurant_config = {
                'restaurant_id':restaurant_id,
                'accessKey':request.form['access_key'],
                'secretKey':request.form['secret_key']
                
            }
            restaurant_config['last_order_id'] = get_last_easi_order(restaurant_config)
            restaurant_config_collection = mongo.db.restaurant_config
            restaurant_config_collection.insert(restaurant_config)
            restaurant_collection.insert(new_restaurant)
    except:
        restaurant_config_collection.delete_one({'restaurant_id':restaurant_id})
    return redirect(url_for('sales.index'))


@sales.route('/delete/restaurant/<restaurant_id>',methods=["POST"])
def delete_restaurant(restaurant_id):
    restaurant_collection = mongo.db.restaurants
    restaurant_config_collection = mongo.db.restaurant_config
    query = {'restaurant_id':restaurant_id}
    restaurant_collection.delete_one(query)

    restaurant_config_collection.delete_one(query)
    return redirect(url_for('sales.index'))



@sales.route('/update/restaurant/<restaurant_id>',methods=["POST"])
def update_restaurant(restaurant_id):
    restaurant_collection = mongo.db.restaurants
    
    query = {'restaurant_id':restaurant_id}
    new_params = {'$set':{'restaurant_name':request.form['restaurant_name'],'store_id_by_ck':request.form['store_id_by_ck'],'restaurant_currency':request.form['restaurant_currency'],'restaurant_country' : request.form['restaurant_country']}}
    store_id_by_ck = request.form['store_id_by_ck']
    res_obj = restaurant_collection.find_one({'store_id_by_ck':store_id_by_ck})   
    if res_obj:
        if res_obj['restaurant_id']!=restaurant_id:
            print('Error')
            return redirect(url_for('sales.index'))
    
    restaurant_collection.update_one(query, new_params)
    
    return redirect(url_for('sales.index'))








