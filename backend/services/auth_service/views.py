import json

from .models import Users
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import logging
from django.contrib.auth import authenticate
from .TokenService import generate_access_token, generate_refresh_token


logger = logging.getLogger(__name__)

def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        email = data.get('email')

        if Users.objects.filter(email=email).exists():
            return JsonResponse({'message': 'email already exists'}, status=400)

        hashed_password = make_password(password)
        Users.objects.create(username=email, password=hashed_password, email=email, first_name=first_name, last_name=last_name)
        return JsonResponse({'message': 'user created successfully'}, status=200)

    return JsonResponse({'message': 'invalid request'}, status=400)

def signin(request):
    logger.fatal("Signin request received")
    logger.fatal(request.headers)
    logger.fatal(request.body)
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({'message' : 'Enter your email and password'}, status=400)

        try:
            user = authenticate(request, username=email, password=password)

            if not user:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
            else:
                access_token, access_exp = generate_access_token(user.id, user.email)
                refresh_token, refresh_exp = generate_refresh_token(user.id, user.email)

                token = {
                    "username": user.email,
                    "access_token": {"token": access_token, "expiration_date": access_exp},
                    "refresh_token": {
                        "token": refresh_token,
                        "expiration_date": refresh_exp,
                    },
                }
                user.refresh_token = refresh_token
                user.access_token = access_token
                user.save()

                return JsonResponse(
                    {"access_token": access_token}, status=200)
        except Exception as e:
            logger.error(f"Error in signin: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def reset_password(request):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            confirm_password = data.get("confirm_password")

            if not email or not password or not confirm_password:
                return JsonResponse({"error": "Email, password, and confirm password are required"}, status=400)

            if password != confirm_password:
                return JsonResponse({"error": "Passwords do not match"}, status=400)

            # Kullanıcıyı bul ve şifreyi güncelle
            user = Users.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"error": "User not found"}, status=404)

            user.set_password(password)
            user.save()
            return JsonResponse({"message": "Password reset successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Error in reset_password: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

