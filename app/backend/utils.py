import uuid
from ..extensions import mongo
length_uid = 14
def generate_user_id():
    id = uuid.uuid4()
    
    
    user_id = str(id.int)[:length_uid]
    
    
    
    user_collection = mongo.db.users
    
    user = user_collection.find({'user_id':user_id})
    if not user:
        user_id = generate_user_id()
    return user_id


length_admin_key = 18
def generate_admin_key():
    id = uuid.uuid4()
    print(id)
    
    admin_key = str(id.int)[:length_admin_key]
    
    
    
    user_collection = mongo.db.users
    
    user = user_collection.find({'admin_key':admin_key})
    if not user:
        admin_key = generate_admin_key()
    return admin_key