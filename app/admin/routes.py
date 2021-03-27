from flask import Blueprint ,request , render_template,redirect,url_for,session

from .utils import generate_partner_id,generate_user_id,generate_restaurant_id,add_justo_res,register_goomer_webhook , get_last_easi_order

from passlib.hash import pbkdf2_sha256

import datetime as dt
from datetime import timezone
from ..extensions import mongo
from ..settings.settings import GOOMER_INTEGRATION_TOKEN
from .utils import dashboard_chart
# the blueprint name for the routes accessed by admin user is admin
admin = Blueprint('admin', __name__, url_prefix='/admin')


#Here are the list of routes that admin user can use


@admin.route('/csm_admin',methods=["GET"])
def csm_index():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))
    
    user_collection = mongo.db.users
    user = user_collection.find_one({'user_id':session['user_id']})
    
    if not user or user['user_permissions']!=1:
        return redirect(url_for('login_page'))


    user_details = {'first_name':user['first_name'],
                    'last_name':user['last_name'],
                    'email':user['email_id'],
                    'designation':'Admin'
                    }

    all_users = user_collection.find({"user_permissions":2,"created_by":user['user_id']})
    lastupdated_bydict = {}
    lis_user = []
    for each_user in all_users:
        user_obj = {
            'user_id':str(each_user['user_id']),
            'user_name':each_user['first_name']+' '+each_user['last_name'],
            'user_email':each_user['email_id'],
            'last_name':each_user['last_name'],
            'first_name':each_user['first_name']
            
            
        }
        if 'last_updated_on' in each_user.keys():

            user_obj['last_updated_on'] = each_user['last_updated_on'].strftime('%I:%M %p %d/%b/%y')
        else:
            user_obj['last_updated_on'] = each_user['created_on'].strftime('%I:%M %p %d/%b/%y')
        # if 'last_updated_by' in each_user:

        #     last_updated_by_id = each_user['last_updated_by']
        #     if last_updated_by_id in lastupdated_bydict.keys():
        #         last_updated_by= lastupdated_bydict[last_updated_by_id]
                
        #     else:

        #         last_update_user = user_collection.find_one({'user_id':last_updated_by_id})
                
        #         last_updated_by_email = last_update_user['email_id']
                
        #         lastupdated_bydict[last_updated_by_id]=last_updated_by_email

            
        #     user_obj['last_updated_by'] = last_updated_by_email
            
        
        # else:
            
        #     user_obj['last_updated_by'] = ''
        
        lis_user.append(user_obj)
    
    return render_template('admin/csm.html',user_permission= user['user_permissions'],user_details=user_details,signout_url = url_for('login_page'),lis_user = lis_user,restaurant_url =url_for('admin.index'),csm_url =url_for('admin.csm_index'))





@admin.route('/add_user',methods=["POST"])
def add_user():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))
    user_collection = mongo.db.users
    user = user_collection.find_one({'user_id':session['user_id']})
    
    if not user or user['user_permissions']!=1:
        return redirect(url_for('login_page'))
    
    email_id = request.form.get('email')
    user_already = user_collection.find_one({'email_id':email_id})
    if user_already:
        return redirect(url_for('admin.csm_index'))
    user_id = generate_user_id()
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')
    created_on = dt.datetime.now(tz=timezone.utc)
    user_permissions = 2
    is_active = False
    last_updated_on = created_on

    new_user = {'user_id':user_id,
    'first_name':first_name,
    'last_name':last_name,
    'email_id':email_id,
    'password':pbkdf2_sha256.encrypt(password),
    'created_on':created_on,
    'created_by':user['user_id'],
    'user_permissions':user_permissions,
    'last_updated_on':last_updated_on,
    'last_updated_by':user['user_id'],
    'is_active':is_active}

    user_collection.insert(new_user)

    return redirect(url_for('admin.csm_index'))



@admin.route('/delete/<user_id>',methods=["POST"])
def delete_user(user_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))
    user_collection = mongo.db.users
    user = user_collection.find_one({'user_id':session['user_id']})
    
    if not user or user['user_permissions']!=1:
        return redirect(url_for('login_page'))

    query = {'user_id':user_id}
    user_collection.delete_one(query)
    return redirect(url_for('admin.csm_index'))




@admin.route('/update/<user_id>', methods=["POST"])
def update_user(user_id):
    
    
    if 'logged_in' not in session or not session['logged_in']:
    
        return redirect(url_for('login_page'))
    user_collection = mongo.db.users
    user = user_collection.find_one({'user_id':session['user_id']})
    
    if not user or user['user_permissions']!=1:
        return redirect(url_for('login_page'))
    last_updated_on = dt.datetime.now(tz=timezone.utc)
    
    if request.form['password']=='':
    
        new_user = {'user_id':user_id,
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email_id':request.form['user_email'],
        # 'password':pbkdf2_sha256.encrypt(request.form['password']),
        'last_updated_on':last_updated_on,
        'last_updated_by':user['user_id']
        }
    else:
        new_user = {'user_id':user_id,
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email_id':request.form['user_email'],
        'password':pbkdf2_sha256.encrypt(request.form['password']),
        'last_updated_on':last_updated_on,
        'last_updated_by':user['user_id']
        }
    return redirect(url_for('admin.csm_index'))


@admin.route('/index',methods=["GET"])
def index():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))
    
    user = mongo.db.users.find_one({'user_id':session['user_id']})
    
    if not user or user['user_permissions']!=1:
        return redirect(url_for('login_page'))

    restaurant_collection = mongo.db.restaurants
    partner_collection = mongo.db.partners
    user_collection =mongo.db.users

    lis_partner = partner_collection.find()
    d={}
    for each_partner in lis_partner:
        d[each_partner['partner_id']] = each_partner['partner_name']

    
    user_details = {'first_name':user['first_name'],
                    'last_name':user['last_name'],
                    'email':user['email_id'],
                    'designation':'Admin'
                    }

    
    all_users = user_collection.find({"user_permissions":2,"created_by":user['user_id']})

    # case 1 self added restaurant
    list_of_res = restaurant_collection.find({'onboarded_by':user['user_id']})
    passed_lis = []
    lastupdated_by_dict={}

    for res in list_of_res:
        if 'last_updated_by' in res.keys():
            if res['last_updated_by'] in lastupdated_by_dict.keys():
                last_updated_by = lastupdated_by_dict[res['last_updated_by']]
            else:
                last_updated_user = user_collection.find_one({'user_id':res['last_updated_by']})
                last_updated_by = last_updated_user['email_id']
                lastupdated_by_dict[res['onboarded_by']] = last_updated_by
        elif res['onboarded_by'] in lastupdated_by_dict.keys():
            last_updated_by = lastupdated_by_dict[res['onboarded_by']]
        else:
            onboarded_user = user_collection.find_one({'user_id':res['onboarded_by']})
            if onboarded_user:

                last_updated_by = onboarded_user['email_id']
                lastupdated_by_dict[res['onboarded_by']] = last_updated_by
            else:
                last_updated_by = ''
                lastupdated_by_dict[res['onboarded_by']] = last_updated_by
        if 'last_updated_on' in res.keys():
            last_updated_on = res['last_updated_on']
        else:
            last_updated_on = res['onboarded_on']
        
        res_obj = {
            'restaurant_id':res['restaurant_id'],
            'store_id_by_ck':res['store_id_by_ck'],
            'restaurant_name':res['restaurant_name'],
            'restaurant_onboarded_by':last_updated_by,
            'restaurant_onboarded_on':last_updated_on.strftime('%I:%M %p %d/%b/%y'),
            'restaurant_currency':res['restaurant_currency'],
            'restaurant_country':res['restaurant_country'],
            'res_partners':d[res['partner_id']]
        }
        
        passed_lis.append(res_obj)
    
    # case2 restaurant added by sales  which are added by self

    for each_user in all_users:
        list_of_res = restaurant_collection.find({'onboarded_by':each_user['user_id']})
        

        for res in list_of_res:
            if 'last_updated_by' in res.keys():
                if res['last_updated_by'] in lastupdated_by_dict.keys():
                    last_updated_by = lastupdated_by_dict[res['last_updated_by']]
                else:
                    last_updated_user = user_collection.find_one({'user_id':res['last_updated_by']})
                    last_updated_by = last_updated_user['email_id']
                    lastupdated_by_dict[res['onboarded_by']] = last_updated_by
            elif res['onboarded_by'] in lastupdated_by_dict.keys():
                last_updated_by = lastupdated_by_dict[res['onboarded_by']]
            else:
                onboarded_user = user_collection.find_one({'user_id':res['onboarded_by']})
                if onboarded_user:

                    last_updated_by = onboarded_user['email_id']
                    lastupdated_by_dict[res['onboarded_by']] = last_updated_by
                else:
                    last_updated_by = ''
                    lastupdated_by_dict[res['onboarded_by']] = last_updated_by
            if 'last_updated_on' in res.keys():
                last_updated_on = res['last_updated_on']
            else:
                last_updated_on = res['onboarded_on']
            
            res_obj = {
                'restaurant_id':res['restaurant_id'],
                'store_id_by_ck':res['store_id_by_ck'],
                'restaurant_name':res['restaurant_name'],
                'restaurant_onboarded_by':last_updated_by,
                'restaurant_onboarded_on':last_updated_on.strftime('%I:%M %p %d/%b/%y'),
                'restaurant_currency':res['restaurant_currency'],
                'restaurant_country':res['restaurant_country'],
                'res_partners':d[res['partner_id']]
            }
            
            passed_lis.append(res_obj)



    return render_template('admin/index.html',user_permission =  user['user_permissions'],list_res=passed_lis[::-1],user_details=user_details,signout_url = url_for('login_page'),csm_url =url_for('admin.csm_index'),restaurant_url =url_for('admin.index'))



@admin.route('/add_restaurant',methods=['POST'])
def add_restaurant():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))
    
    user = mongo.db.users.find_one({'user_id':session['user_id']})
    
    if not user or user['user_permissions']!=1:
        return redirect(url_for('login_page'))

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
        return redirect(url_for('admin.index'))
    
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
    return redirect(url_for('admin.index'))


@admin.route('/delete/restaurant/<restaurant_id>',methods=["POST"])
def delete_restaurant(restaurant_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))
    user_collection = mongo.db.users
    user = user_collection.find_one({'user_id':session['user_id']})
    
    if not user or user['user_permissions']!=1:
        return redirect(url_for('login_page'))

    restaurant_collection = mongo.db.restaurants
    restaurant_config_collection = mongo.db.restaurant_config

    query = {'restaurant_id':restaurant_id}
    restaurant_collection.delete_one(query)

    restaurant_config_collection.delete_one(query)

    return redirect(url_for('admin.index'))



@admin.route('/update/restaurant/<restaurant_id>',methods=["POST"])
def update_restaurant(restaurant_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))
    user_collection = mongo.db.users
    user = user_collection.find_one({'user_id':session['user_id']})
    
    if not user or user['user_permissions']!=1:
        return redirect(url_for('login_page'))
    restaurant_collection = mongo.db.restaurants
    
    query = {'restaurant_id':restaurant_id}
    new_params = {'$set':{'last_updated_by':user['user_id'],'last_updated_on':dt.datetime.now(tz=timezone.utc),'restaurant_name':request.form['restaurant_name'],'store_id_by_ck':request.form['store_id_by_ck'],'restaurant_currency':request.form['restaurant_currency'],'restaurant_country' : request.form['restaurant_country']}}
    store_id_by_ck = request.form['store_id_by_ck']
    res_obj = restaurant_collection.find_one({'store_id_by_ck':store_id_by_ck})   
    if res_obj:
        if res_obj['restaurant_id']!=restaurant_id:
            print('Error')
            return redirect(url_for('admin.index'))
    
    restaurant_collection.update_one(query, new_params)
    
    return redirect(url_for('admin.index'))
    

