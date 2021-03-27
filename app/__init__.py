from flask import Flask,jsonify,render_template,session
from flask import redirect , url_for
# from flask_login import LoginManager 
import datetime



# importing all the blue prints
from .Justo.routes import justo_webhook as justo
from .sales.routes import sales
from .backend.routes import backend
from .admin.routes import admin
from .login.routes import login
from .super_admin.routes import super_admin

from .goomer.routes import goomer_webhook as goomer
from .Easi.routes import easi_webhook as easi
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
    app.register_blueprint(justo)
    app.register_blueprint(goomer)
    app.register_blueprint(sales)
    app.register_blueprint(backend)
    app.register_blueprint(admin)
    app.register_blueprint(super_admin)
    app.register_blueprint(login)
    app.register_blueprint(easi)

    @app.route('/')
    def login_page():
        session.pop('user_id', None)
        session['logged_in'] = False
        return render_template('login.html',url_forgot ='forgot_password.html')


    
    return app

