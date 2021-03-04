from functools import wraps
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from flask import request, session, g
import json
import base64

def google_auth(f):
    @wraps(f)
    def googleAuthFunction(*args, **kwargs):
        if request.headers.get('Authorization') is not None:
            decodedBytes = base64.b64decode(request.headers.get('Authorization'))
            decodedStr = str(decodedBytes, 'ascii')
            credentials = Credentials.from_authorized_user_info(
                json.loads(decodedStr))
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            g.googleUser = credentials
        return f(*args, **kwargs)
    return googleAuthFunction
