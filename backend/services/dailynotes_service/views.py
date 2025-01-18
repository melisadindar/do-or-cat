import json
import re
from .models import Dailynotes
from django.http import JsonResponse
from services.auth_service.models import Users
from services.auth_service.TokenService import get_current_user

def create_dailynotes(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        description = data.get('description')

        if not description:
            return JsonResponse({'message': 'Enter your email and description'}, status=400)
        
        try:
            user = get_current_user(request)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=401)
        
        Dailynotes.objects.create(user=user, description=description)
        return JsonResponse({'message': 'Daily note created successfully'}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)

def get_dailynotes(request):
    if request.method == 'GET':

        try:
            user = get_current_user(request)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=401)
        
        notes = Dailynotes.objects.filter(user=user)
        notes_list = []
        for note in notes:
            notes_list.append({
                'description': note.description,
                'mission_date': note.mission_date,
                'created_at': note.created_at,
                'updated_at': note.updated_at
            })
        return JsonResponse({'notes': notes_list}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)

def delete_dailynotes(request):
    if request.method == 'DELETE':


        try:
            user = get_current_user(request)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=404)
        
        try:
            note = Dailynotes.objects.get(user=user)
        except Dailynotes.DoesNotExist:
            return JsonResponse({'message': 'Note not found'}, status=404)
        
        note.delete()
        return JsonResponse({'message': 'Note deleted successfully'}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)


def delete_multiply_dailynotes(request):
    if request.method == 'DELETE':

        try:
            user = get_current_user(request)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=404)

        try:
            note = Dailynotes.objects.get(user=user)
        except Dailynotes.DoesNotExist:
            return JsonResponse({'message': 'Note not found'}, status=404)
        
        note.delete()
        return JsonResponse({'message': 'Notes deleted successfully'}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)

def update_dailynotes(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        description = data.get('description')
        mission_date = data.get('mission_date')

        try:
            user = get_current_user(request)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=404)
        
        try:
            note = Dailynotes.objects.get(user=user)
        except Dailynotes.DoesNotExist:
            return JsonResponse({'message': 'Note not found'}, status=404)
        
        note.description = description
        note.mission_date = mission_date
        note.save()
        return JsonResponse({'message': 'Note updated successfully'}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)
