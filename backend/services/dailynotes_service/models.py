from django.db import models
from services.auth_service.models import Users

class Dailynotes(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='daily_notes', default=1)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mission_date = models.DateField(null=True, blank=True)