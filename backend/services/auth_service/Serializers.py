from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed
from services.auth_service.models import Users

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("username")  # 'username' yerine email'i kullanıyoruz.
        password = attrs.get("password")

        # Kullanıcıyı email üzerinden al
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            raise AuthenticationFailed("User not found")

        # Parola doğrulaması
        if not check_password(password, user.password):
            raise AuthenticationFailed("Incorrect password")

        # JWT oluştur ve kullanıcı bilgilerini ekle
        data = super().validate({
            "username": user.email,  # Burada 'username' SimpleJWT gerekliliği için kullanılıyor.
            "password": password
        })

        data["email"] = user.email
        data["username"] = user.username
        data["first_name"] = user.first_name
        data["last_name"] = user.last_name

        return data
