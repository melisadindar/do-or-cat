import os
import logging
import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
import json

from services.mail_service.models import reset_codes
from django.views.decorators.csrf import csrf_exempt

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

            code = generate_random_code()
            cache.set(f"password_reset_code_{email}", code, timeout=300)  # Kod 5 dakika geçerli
            subject = "Password Reset Code"
            message = f"Your password reset code is {code}"
            send_email(email, subject, message)
            reset_codes.objects.create(reciever_mail=email, code=code)

            return JsonResponse({"message": "Password reset email sent successfully"}, status=200)
        except Exception as e:
            logger.error(f"Error in send_password_mail_view: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def verify_reset_code(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            email = body.get("email")
            code = body.get("code")

            if not email or not code:
                return JsonResponse({"error": "Email and code are required"}, status=400)

            # Cache'den kodu al
            cached_code = cache.get(f"password_reset_code_{email}")
            if cached_code and cached_code == code:
                return JsonResponse({"message": "Code verified successfully"}, status=200)

            # Cache'de yoksa veritabanını kontrol et
            reset_code_entry = reset_codes.objects.filter(reciever_mail=email, code=code).first()
            if reset_code_entry:
                return JsonResponse({"message": "Code verified successfully"}, status=200)

            return JsonResponse({"error": "Invalid code or expired"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Error in verify_reset_code: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


