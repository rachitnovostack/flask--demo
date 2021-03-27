from flask import Blueprint ,request

import datetime
from datetime import timezone
from .utils import generate_user_id

from ..extensions import mongo

# the blueprint name for the routes accessed by dashboard user is dboard
dboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dboard.route('/add_user',methods=["POST"])
def add_user():
    user_collection = mongo.db.users
    
    email_id = request.form.get('email')
    user_already = user_collection.find({'email_id':email_id})
    if not user_already:
        return {"Error":"User already present"}
    user_id = generate_user_id()
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')
    created_on = datetime.datetime.now(tz=timezone.utc)
    user_permissions = request.form.get('permission_id')
    is_active = False
    last_updated_on = created_on

    return {'success':1}