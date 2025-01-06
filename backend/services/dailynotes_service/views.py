import json
from .models import dailynotes
from django.http import JsonResponse
from services.auth_service.models import Users

def create_dailynotes(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        owner_mail = data.get('owner_mail')
        description = data.get('description')

        if not owner_mail or not description:
            return JsonResponse({'message': 'Enter your email and description'}, status=400)
        
        try:
            user = Users.objects.get(email=owner_mail)
        except Users.DoesNotExist:
            return JsonResponse({'message' : 'User not found'}, status=404)
        
        dailynotes.objects.create(owner_mail=user, description=description)
        return JsonResponse({'message': 'Daily note created successfully'}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)