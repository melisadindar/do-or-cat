import os
import logging
import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
import json
from services.auth_service.TokenService import get_current_user

from services.mail_service.models import reset_codes
from django.views.decorators.csrf import csrf_exempt
from services.auth_service.models import Users

logger = logging.getLogger(__name__)

def send_email(email, subject, message):
    from_email = os.environ.get('EMAIL_HOST_USER')
    if not from_email:
        logger.error("EMAIL_HOST_USER environment variable is not set.")
        raise ValueError("EMAIL_HOST_USER environment variable is not set.")
    
    try:
        send_mail(subject, message, from_email, [email])
        logger.info(f"Email sent to {email} with subject {subject}")
    except Exception as e:
        logger.error(f"Error sending email to {email}: {e}")


def generate_random_code():
    return "".join([str(random.randint(0, 9)) for _ in range(4)])


def send_password_mail(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            email = body.get("email")
            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)
            
            user = Users.objects.filter(email=email).first()

            code = generate_random_code()
            cache.set(f"password_reset_code_{user.email}", code, timeout=300)  # Kod 5 dakika geçerli
            subject = "Password Reset Code"
            message = f"Your password reset code is {code}"
            send_email(email, subject, message)
            reset_codes.objects.create(user=user, code=code)

            return JsonResponse({"message": "Password reset email sent successfully"}, status=200)
        except Exception as e:
            logger.error(f"Error in send_password_mail_view: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def verify_reset_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code")

            if not code:
                return JsonResponse({"error": "Email and code are required"}, status=400)
            
            current_user = get_current_user(request)
            if not current_user:
                return JsonResponse({"error": "Unauthorized"}, status=401)

            # Cache'den kodu al
            cached_code = cache.get(f"password_reset_code_{current_user.email}")
            if cached_code and cached_code == code:
                return JsonResponse({"message": "Code verified with cache successfully"}, status=200)

            # Cache'de yoksa veritabanını kontrol et
            reset_code_entry = reset_codes.objects.filter(user=current_user, code=code).first()
            if reset_code_entry and reset_code_entry.is_valid():
                return JsonResponse({"message" : "Code is valid"}, status=200)
            else:
                return JsonResponse({"error": "Invalid code or expired"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Error in verify_reset_code: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


