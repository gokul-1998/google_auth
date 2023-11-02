from dotenv import load_dotenv
load_dotenv()
import os

name='google'
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
access_token_url='https://accounts.google.com/o/oauth2/token'
access_token_params=None
authorize_url='https://accounts.google.com/o/oauth2/auth'
authorize_params=None
api_base_url='https://www.googleapis.com/oauth2/v1/'
userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo'