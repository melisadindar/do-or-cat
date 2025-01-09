from django.db import models

class dailynotes(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    reciever_mail = models.EmailField(max_length=254, default='default@example.com')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mission_date = models.DateField(null=True, blank=True)