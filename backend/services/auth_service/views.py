import json
from .models import Users
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password


def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if Users.objects.filter(username=username).exists():
            return JsonResponse({'message': 'username already exists'})
        if Users.objects.filter(email=email).exists():
            return JsonResponse({'message': 'email already exists'})

        hashed_password = make_password(password)
        Users.objects.create(username=username, password=hashed_password, email=email, first_name=first_name, last_name=last_name)
        return JsonResponse({'message': 'user created successfully'})

    return JsonResponse({'message': 'invalid request'})

def signin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({'message' : 'Enter your email and password'}, status=400)

        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return JsonResponse({'message' : 'User not found'}, status=404)

        if not check_password(password, user.password):
            return JsonResponse({'message' : 'Incorrect password'}, status=400)
        
        return JsonResponse({'message' : 'Sign in is succes'}, status=200)
    return JsonResponse({'message': 'invalid request'})



