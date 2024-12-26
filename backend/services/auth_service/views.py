import json
from .models import Users
from django.http import JsonResponse

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

        Users.objects.create(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        return JsonResponse({'message': 'user created successfully'})

    return JsonResponse({'message': 'unvalid request'})


def signin(request):
    if request == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = Users.objects.get(username=username)
        if user and user.check_password(password):
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message': 'failed'})



