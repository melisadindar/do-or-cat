import jwt
from datetime import datetime, timedelta
import os
from services.auth_service.models import Users
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv('SECRET_KEY')


def generate_access_token(user_id, email):
    expiration_time = datetime.utcnow() + timedelta(days=2)
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=2),
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token, expiration_time

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token expired. Please log in again.(Expired)')  
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token. Please log in again.(Invalid)')
    
def get_current_user(request):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            logger.error("Authorization header is missing or improperly formatted.")
            raise ValueError("Invalid Authorization header.")
        token = auth_header.split(' ')[1]
        logger.info(f"Received token: {token}")
    except IndexError:
        logger.error("Malformed Authorization header.")
        raise ValueError("Authorization header is malformed or missing token.")
    
    payload = verify_token(token)
    user_id = payload.get('user_id')

    if not payload:
        raise ValueError("Invalid token, no payload found.")
        
    # Kullanıcıyı Users modelinden al
    try:
        user = Users.objects.get(id=user_id)
        return user
    except Users.DoesNotExist:
        raise ValueError("User not found.")



def refresh_access_token(token):
    payload = verify_token(token)
    user_id = payload.get('user_id')
    email = payload.get('email')
    return generate_access_token(user_id, email)

def generate_refresh_token(user_id, email):
    expiration_time = datetime.utcnow() + timedelta(days=7)  # Örnek olarak 7 gün geçerli
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': expiration_time,
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token, expiration_time