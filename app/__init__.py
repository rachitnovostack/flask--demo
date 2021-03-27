from flask import Flask,jsonify,render_template,session
from flask import redirect , url_for
# from flask_login import LoginManager 
import datetime



# importing all the blue prints
from .sales.routes import sales

from .admin.routes import admin
from .login.routes import login
from .super_admin.routes import super_admin


# from .models import user

# from flask_login import UserMixin

from .extensions import mongo   

# creating our flask app
def create_app():

    # configuring the app with config.py 
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')
    
    # adding flask-pymongo to app
    mongo.init_app(app)
    
    
    
    # registering all the blueprints
    
    app.register_blueprint(sales)

    app.register_blueprint(admin)
    app.register_blueprint(super_admin)
    app.register_blueprint(login)
    

    @app.route('/')
    def login_page():
        session.pop('user_id', None)
        session['logged_in'] = False
        return render_template('login.html',url_forgot ='forgot_password.html')


    
    return app

