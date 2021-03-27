from flask import Blueprint ,request , render_template ,session
from passlib.hash import pbkdf2_sha256
import jwt,os

import datetime

from ..extensions import mongo,mail
from flask_mail import Message
from .sender import send_mail
from flask import render_template,url_for,redirect
# the blueprint name for the routes accessed by sales user is sales
login = Blueprint('login', __name__, url_prefix='/login')


@login.route('/',methods=["POST","GET"])
def login_user():
    if request.method=="GET":
        return redirect(url_for('login_page'))
    session.pop('user_id', None)
    session.pop('logged_in',None)
    users_collection = mongo.db.users
    user_email = request.form['email']
    password = request.form['password']
    user = users_collection.find_one({'email_id':user_email})
    # add in seesion
    
    if user and pbkdf2_sha256.verify(password, user['password']):
        session['user_id'] = user['user_id']
        session['logged_in'] = True
        if user['user_permissions']==2:
            return redirect(url_for('sales.index'))
        elif user['user_permissions']==1:
            return redirect(url_for('admin.index'))
        elif user['user_permissions']==3:
            return redirect(url_for('super_admin.index'))
    # redirect to '/' location of the user
    return render_template('login.html')


@login.route('/forgot_password',methods=["GET","POST"])
def forgot_password():
    if request.method=="GET":
        
        return render_template('forgot_password.html')
    # send confirmation email
    user_email = request.form['email']
    users_collection = mongo.db.users
    user = users_collection.find({'email_id':user_email})
    if not user:
        return redirect(url_for('login_page'))


    token = get_reset_token(user_email)
    # url = url_for('login.validate_token',token=token,external=True)
    url = 'http://127.0.0.1:5000/login/validate_token/'+token.decode()
    send_mail(user_email,url)
    return redirect(url_for('login_page'))

def get_reset_token(user_email):
    return jwt.encode({'user_email': user_email,
                        'exp':   datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                        key='Sm9obiBTY2hyb20ga2lja3MgYXNz')



def verify_reset_token(token):
    token = token.encode()
    try:
        user_email = jwt.decode(token,key='Sm9obiBTY2hyb20ga2lja3MgYXNz')['user_email']
    except Exception as e:
        
        return False,_
    return True,user_email



@login.route('/validate_token/<token>',methods=["GET"])
def validate_token(token):
    boo,user_email = verify_reset_token(token)
    if boo:
        users_collection = mongo.db.users
        user = users_collection.find_one({'email_id':user_email})
        if user:

            return render_template('reset_password.html',token=token)
    
    return redirect(url_for('login_page'))


@login.route('/reset_password/<token>',methods=['POST'])
def reset_password(token):
    boo,user_email = verify_reset_token(token)
    if boo:
        users_collection = mongo.db.users
        user = users_collection.find_one()
        new_password = request.form['confirm_password']
        query = {'email_id':user_email}
        new_params = {'$set':{'password':pbkdf2_sha256.encrypt(new_password)}}
        users_collection.update_one(query, new_params)


    return redirect(url_for('login_page'))