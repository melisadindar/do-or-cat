import json
from .models import Notes
from django.http import JsonResponse
from services.auth_service.models import Users

def create_notes(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        reciever_mail = data.get('reciever_mail')
        title = data.get('title')
        description = data.get('description')

        if not title or not description:
            return JsonResponse({'message': 'Enter title and description'}, status=400)
        
        try:
            user = Users.objects.get(email=reciever_mail)
        except Users.DoesNotExist:
            return JsonResponse({'message' : 'User not found'}, status=404)
        
        Notes.objects.create(title=title, description=description, reciever_mail=user)
        return JsonResponse({'message': 'Note created successfully'}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)

