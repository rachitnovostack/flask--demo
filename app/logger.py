from .extensions import mongo

class BaseLoggerObj():

    def __init__(self,partner_id,store_id,restaurant_id,order_id,order_state,error_message,trial_times,last_seen,response_code):
        self.partner_id = partner_id
        self.store_id_by_ck = store_id
        self.restaurant_id = restaurant_id
        self.order_id= order_id
        self.order_state = order_state
        self.error_message = error_message
        self.trial_times =trial_times
        self.last_seen = last_seen
        self.response_code = response_code

    def write(self):
        data_transformer = mongo.db.data_transformer

        new_query = {
        'partner_id': self.partner_id,
        'store_id_by_ck': self.store_id_by_ck,
        'restaurant_id': self.restaurant_id,
        'order_id': self.order_id,
        'order_state': self.order_state,
        
        'error_message': self.error_message,
        'trial_times': self.trial_times,
        'last_seen': self.last_seen,
        'response_code': self.response_code
        
        }
        data_transformer.insert(new_query)
        

class BaseLoggerWithCallbackObj():
    
    def __init__(self,partner_id,store_id,restaurant_id,order_id,order_state,error_message,trial_times,last_seen,response_code,order_accept_resp_code):
        self.partner_id = partner_id
        self.store_id_by_ck = store_id
        self.restaurant_id = restaurant_id
        self.order_id= order_id
        self.order_state = order_state
        self.error_message = error_message
        self.trial_times =trial_times
        self.last_seen = last_seen
        self.response_code = response_code
        self.order_accept_resp_code = order_accept_resp_code

    def write(self):
        data_transformer = mongo.db.data_transformer

        new_query = {
        'partner_id': self.partner_id,
        'store_id_by_ck': self.store_id_by_ck,
        'restaurant_id': self.restaurant_id,
        'order_id': self.order_id,
        'order_state':self.order_state,
        
        'error_message': self.error_message,
        'trial_times': self.trial_times,
        'last_seen': self.last_seen,
        'response_code': self.response_code,
        'order_accept_resp_code':self.order_accept_resp_code
        }
        data_transformer.insert(new_query)

class UpdateRequestLogger():
    def __init__(self,partner_id,store_id,restaurant_id,order_id,order_state,order_status_mapping,error_message,trial_times,last_seen,response_code):
        self.partner_id = partner_id
        self.store_id_by_ck = store_id
        self.restaurant_id = restaurant_id
        self.order_id= order_id
        self.order_state = order_state
        self.order_status_mapping = order_status_mapping
        self.error_message = error_message
        self.trial_times =trial_times
        self.last_seen = last_seen
        self.response_code = response_code
        

    def write(self):
        data_transformer = mongo.db.data_transformer

        new_query = {
        'partner_id': self.partner_id,
        'store_id_by_ck': self.store_id_by_ck,
        'restaurant_id': self.restaurant_id,
        'order_id': self.order_id,
        'order_state':self.order_state,
        'order_status_mapping':self.order_status_mapping,
        'error_message': self.error_message,
        'trial_times': self.trial_times,
        'last_seen': self.last_seen,
        'response_code': self.response_code
        
        }
        data_transformer.insert(new_query)