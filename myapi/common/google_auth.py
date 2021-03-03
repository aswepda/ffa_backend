from functools import wraps
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from flask import request, session, g
import json

def google_auth(f):
    @wraps(f)
    def googleAuthFunction(*args, **kwargs):
        if session.get('googleSession') is not None:
            credentials = Credentials.from_authorized_user_info(
                json.loads(session['googleSession']))
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            g.googleUser = credentials
        return f(*args, **kwargs)
    return googleAuthFunction
