from .goomer_config import *

GOOMER_DEVELOPMENT = True
GOOMER_STAGING = True
GOOMER_PRODUCTION = False


if GOOMER_PRODUCTION:
    GOOMER_AUTH_URL = GOOMER_AUTH_URL_PROD
    GOOMER_REFRESH_TOKEN_URL = GOOMER_REFRESH_TOKEN_URL_PROD
    GOOMER_ORDER_DETAILS_URL = GOOMER_ORDER_DETAILS_URL_PROD
    GOOMER_ORDER_CALLBACK_URL = GOOMER_ORDER_CALLBACK_URL_PROD
    GOOMER_WEBHOOK_REGISTER_URL = GOOMER_WEBHOOK_REGISTER_URL_PROD
    GOOMER_INTEGRATION_TOKEN = GOOMER_INTEGRATION_TOKEN_PROD

elif GOOMER_STAGING:
    GOOMER_AUTH_URL = GOOMER_AUTH_URL_STAGING
    GOOMER_REFRESH_TOKEN_URL = GOOMER_REFRESH_TOKEN_URL_STAGING
    GOOMER_ORDER_DETAILS_URL = GOOMER_ORDER_DETAILS_URL_STAGING
    GOOMER_ORDER_CALLBACK_URL = GOOMER_ORDER_CALLBACK_URL_STAGING
    GOOMER_WEBHOOK_REGISTER_URL = GOOMER_WEBHOOK_REGISTER_URL_STAGING
    GOOMER_INTEGRATION_TOKEN = GOOMER_INTEGRATION_TOKEN_STAGING
 
else:
    
    # default is staging for goomer
    GOOMER_AUTH_URL = GOOMER_AUTH_URL_STAGING
    GOOMER_REFRESH_TOKEN_URL = GOOMER_REFRESH_TOKEN_URL_STAGING
    GOOMER_ORDER_DETAILS_URL = GOOMER_ORDER_DETAILS_URL_STAGING
    GOOMER_ORDER_CALLBACK_URL = GOOMER_ORDER_CALLBACK_URL_STAGING
    GOOMER_WEBHOOK_REGISTER_URL = GOOMER_WEBHOOK_REGISTER_URL_STAGING
    GOOMER_INTEGRATION_TOKEN = GOOMER_INTEGRATION_TOKEN_STAGING