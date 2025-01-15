import jwt
from datetime import datetime, timedelta
import os
from rest_framework.authtoken.models import Token

SECRET_KEY = os.getenv('SECRET_KEY')

def generate_token(user_id, email):
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=2),
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token expired. Please log in again.')  
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token. Please log in again.')
    
# Token doğrulama işlemi:
def get_current_user(request):
    token_key = request.headers.get('Authorization')
    if not token_key:
        raise ValueError("Token is missing")
    
    token = Token.objects.filter(key=token_key).first()
    if not token:
        raise ValueError("Invalid token")
    
    return token.user
