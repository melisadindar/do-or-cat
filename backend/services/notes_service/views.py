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

def get_notes(request):
    if request.method == 'GET':
        data = json.loads(request.body)

        receiver_mail = data.get('reciever_mail')

        try:
            user = Users.objects.get(email=receiver_mail)
        except Users.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
        
        notes = Notes.objects.filter(reciever_mail=user)
        notes_list = []
        for note in notes:
            notes_list.append({
                'title': note.title,
                'description': note.description,
                'created_at': note.created_at,
                'updated_at': note.updated_at
            })
        return JsonResponse({'notes': notes_list}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)

def delete_notes(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)

        receiver_mail = data.get('reciever_mail')
        note_id = data.get('note_id')

        try:
            user = Users.objects.get(email=receiver_mail)
        except Users.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
        
        try:
            note = Notes.objects.get(id=note_id, reciever_mail=user)
        except Notes.DoesNotExist:
            return JsonResponse({'message': 'Note not found'}, status=404)
        
        note.delete()

        return JsonResponse({'message': 'Notes deleted successfully'}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)

def delete_multiply_notes(request):
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
                note = Notes.objects.get(id=note_id, reciever_mail=user)
            except Notes.DoesNotExist:
                return JsonResponse({'message': 'Note not found'}, status=404)
            note.delete()

        return JsonResponse({'message': 'Notes deleted successfully'}, status=200)


def update_notes(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        receiver_mail = data.get('reciever_mail')
        note_id = data.get('note_id')
        title = data.get('title')
        description = data.get('description')

        try:
            user = Users.objects.get(email=receiver_mail)
        except Users.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
        
        try:
            note = Notes.objects.get(id=note_id, reciever_mail=user)
        except Notes.DoesNotExist:
            return JsonResponse({'message': 'Note not found'}, status=404)
        
        note.title = title
        note.description = description
        note.save()

        return JsonResponse({'message': 'Note updated successfully'}, status=200)