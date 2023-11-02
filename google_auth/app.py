from flask import Flask, flash, redirect, url_for, session,render_template,request
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from cred import *

# decorator for routes that should be accessible only by logged in users
# from auth_decorator import login_required
from auth_decorator import login_required



# dotenv setup
'''from dotenv import load_dotenv
load_dotenv()
'''

# App config
app = Flask(__name__)
# Session config
app.secret_key = 'random secret'
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# oAuth Setup
oauth = OAuth(app)
googlte = oauth.register(
    name='google',
    client_id=client_id,
    client_secret=client_secret,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


@app.route("/")
def index():
    for key in list(session.keys()):
        session.pop(key)
    message = request.args.get('message')
    return render_template("index.html",message=message)


@app.route('/dashboard')
@login_required
def hello_world1():
    print(session)
    email = dict(session)['profile']['email']
    name=dict(session)['profile']['given_name']
    
    return f'Hello, you are logge in as {email}!'


@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff you specified in the scope
    user_info = resp.json()
    
    # Check if the user's email domain matches the allowed organization domain
    allowed_domain = 'ds.study.iitm.ac.in'
    user_email = user_info.get('email', '')

    if user_email.endswith('@' + allowed_domain):
        # Here you use the profile/user data that you got and query your database
        # to find/register the user and set your own data in the session, not the profile from Google
        session['profile'] = user_info
        session.permanent = True  # make the session permanent so it keeps existing after the browser gets closed
        return redirect('/dashboard')
    else:
        # Handle the case where the user's email domain is not allowed
        # flash('Only users from {} are allowed to log in.'.format(allowed_domain), 'error')
        return redirect('/?message=Only users from {} are allowed to log in.'.format(allowed_domain))

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)