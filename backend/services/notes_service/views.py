import json

from .models import Notes
from services.auth_service.TokenService import get_current_user
from django.http import JsonResponse

def create_notes(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        title = data.get('title')
        description = data.get('description')

        if not title or not description:
            return JsonResponse({'message': 'Enter title and description'}, status=400)
        
        try:
            user = get_current_user(request)
        except ValueError as e:
            return JsonResponse({'message' : str(e)}, status=404)
        
        Notes.objects.create(title=title, description=description, user=user)
        return JsonResponse({'message': 'Note created successfully'}, status=200)
    return JsonResponse({'message': 'invalid request'}, status=400)

def get_notes(request):
    if request.method == 'GET':

        try:
            user = get_current_user(request)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=401)  # Token geçersizse hata döndür
        
        notes = Notes.objects.filter(user=user)
        
        if not notes:
            return JsonResponse({'message': 'No notes found for this user'}, status=404)

        notes_list = [
            {
                'title': note.title,
                'description': note.description,
                'created_at': note.created_at,
                'updated_at': note.updated_at,
            }
            for note in notes
        ]
        return JsonResponse({'notes': notes_list}, status=200)

    return JsonResponse({'message': 'Invalid request'}, status=400)

def delete_notes(request):
    if request.method == 'DELETE':
        try:
            user = get_current_user(request)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=404)
        
        try:
            note = Notes.objects.get(user=user)
        except Notes.DoesNotExist:
            return JsonResponse({'message': 'Note not found'}, status=404)
        
        note.delete()
        return JsonResponse({'message': 'Notes deleted successfully'}, status=200)
    
    return JsonResponse({'message': 'invalid request'}, status=400)

def delete_multiply_notes(request):
    if request.method == 'DELETE':

        try:
            user = get_current_user(request)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=404)
        
        try:
            note = Notes.objects.get(user=user)
        except Notes.DoesNotExist:
            return JsonResponse({'message': 'Note not found'}, status=404)
        note.delete()

        return JsonResponse({'message': 'Notes deleted successfully'}, status=200)


def update_notes(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        title = data.get('title')
        description = data.get('description')

        try:
            user = get_current_user(request)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=404)
        
        try:
            note = Notes.objects.get(user=user)
        except Notes.DoesNotExist:
            return JsonResponse({'message': 'Note not found'}, status=404)
        
        note.title = title
        note.description = description
        note.save()

        return JsonResponse({'message': 'Note updated successfully'}, status=200)