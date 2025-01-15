from django.db import models
from services.auth_service.models import Users

class Notes(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='notes', default=1)
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

