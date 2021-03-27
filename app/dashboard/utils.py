import uuid

length_uid = 8
def generate_user_id():
    id = uuid.uuid4()
    
    
    user_id = str(id.int)[:length_uid]
    
    
    
    user_collection = mongo.db.users
    
    user = user_collection.find({'user_id':user_id})
    if not user:
        user_id = generate_user_id()
    return user_id