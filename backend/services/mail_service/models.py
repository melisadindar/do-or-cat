from django.db import models

#from services.auth_service.models import Users

class reset_codes(models.Model):
    id = models.AutoField(primary_key=True)
    reciever_mail = models.EmailField()
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

