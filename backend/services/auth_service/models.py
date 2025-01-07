from django.db import models
from django.contrib.auth.hashers import make_password

class Users(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def create(self):
        self.password = make_password(self.password)
        self.save()

    def set_password(self, password):
        self.password = make_password(password)
        self.save()
    
    def __str__(self):
        return self.username
