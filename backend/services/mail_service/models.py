from django.db import models
from django.utils.timezone import now
from datetime import timedelta

#from services.auth_service.models import Users

class reset_codes(models.Model):
    id = models.AutoField(primary_key=True)
    reciever_mail = models.EmailField()
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def is_valid(self):
        return now() < self.created_at + timedelta(minutes=5) #oluşturulma tarihinden 5 dakika geçmediyse True döner