from services.auth_service.models import Users
from django.contrib import admin

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'created_at')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)

admin.site.register(Users, UsersAdmin)