from django.db import models

class Notes(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    reciever_mail = models.EmailField(max_length=254, default='default@example.com')
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

