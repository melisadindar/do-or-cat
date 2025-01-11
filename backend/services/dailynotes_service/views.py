import json
import re
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

def get_dailynotes(request):
    if request.method == 'GET':
        data = json.loads(request.body)

        receiver_mail = data.get('reciever_mail')

        try:
            user = Users.objects.get(email=receiver_mail)
        except Users.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
        
        notes = dailynotes.objects.filter(reciever_mail=user)
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
        data = json.loads(request.body)

        receiver_mail = data.get('reciever_mail')
        note_id = data.get('note_id')

        try:
            user = Users.objects.get(email=receiver_mail)
        except Users.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
        
        try:
            note = dailynotes.objects.get(id=note_id, reciever_mail=user)
        except dailynotes.DoesNotExist:
            return JsonResponse({'message': 'Note not found'}, status=404)
        
        note.delete()
        return JsonResponse({'message': 'Note deleted successfully'}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)


def delete_multiply_dailynotes(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)

        receiver_mail = data.get('reciever_mail')
        note_ids = data.get('note_ids')

        try:
            user = Users.objects.get(email=receiver_mail)
        except Users.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
        
        for note_id in note_ids:
            try:
                note = dailynotes.objects.get(id=note_id, reciever_mail=user)
            except dailynotes.DoesNotExist:
                return JsonResponse({'message': 'Note not found'}, status=404)
            
            note.delete()
        return JsonResponse({'message': 'Notes deleted successfully'}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)

def update_dailynotes(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        receiver_mail = data.get('reciever_mail')
        note_id = data.get('note_id')
        description = data.get('description')
        mission_date = data.get('mission_date')

        try:
            user = Users.objects.get(email=receiver_mail)
        except Users.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
        
        try:
            note = dailynotes.objects.get(id=note_id, reciever_mail=user)
        except dailynotes.DoesNotExist:
            return JsonResponse({'message': 'Note not found'}, status=404)
        
        note.description = description
        note.mission_date = mission_date
        note.save()
        return JsonResponse({'message': 'Note updated successfully'}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)
