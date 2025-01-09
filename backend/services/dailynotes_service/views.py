import json
from .models import dailynotes
from django.http import JsonResponse
from services.auth_service.models import Users

def create_dailynotes(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        reciever_mail = data.get('reciever_mail')
        description = data.get('description')
        mission_date = data.get('mission_date')


        if not reciever_mail or not description:
            return JsonResponse({'message': 'Enter your email and description'}, status=400)
        
        try:
            user = Users.objects.get(email=reciever_mail)
        except Users.DoesNotExist:
            return JsonResponse({'message' : 'User not found'}, status=404)
        
        dailynotes.objects.create(reciever_mail=user, description=description, mission_date=mission_date)
        return JsonResponse({'message': 'Daily note created successfully'}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)