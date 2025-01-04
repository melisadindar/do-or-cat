import json
from .models import Users
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password


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

    return JsonResponse({'message': 'unvalid request'})

def signin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not Users.objects.filter(username=username).exists():
            return JsonResponse({'message': 'user not found'})
        
        if not Users.objects.filter(password=password).exists():
            return JsonResponse({'message': 'password is incorrect'})

        user = Users.objects.get(username=username, password=password)
        if user:
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message': 'failed'})
    return JsonResponse({'message': 'unvalid request'})



