from functools import wraps
from flask import session, redirect, url_for

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'profile' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function