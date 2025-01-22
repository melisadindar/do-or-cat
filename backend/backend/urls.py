"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path
from services.auth_service import views as auth_views
from services.dailynotes_service import views as dailynotes_views
from services.notes_service import views as notes_views
from services.mail_service import views as mail_views
from services.auth_service import TokenService as token_service

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('auth_service/signup/', auth_views.signup),
    path('auth_service/signin/', auth_views.signin),

    path('notes_service/create_notes/', notes_views.create_notes),
    path('notes_service/get_notes/', notes_views.get_notes),
    path('notes_service/delete_notes/', notes_views.delete_notes),
    path('notes_service/delete_multiply_notes/', notes_views.delete_multiply_notes),
    path('notes_service/update_notes/', notes_views.update_notes),
    
    path('dailynotes_service/create_dailynotes/', dailynotes_views.create_dailynotes),
    path('dailynotes_service/get_dailynotes/', dailynotes_views.get_dailynotes),
    path('dailynotes_service/delete_dailynotes/', dailynotes_views.delete_dailynotes),
    path('dailynotes_service/delete_multiply_dailynotes/', dailynotes_views.delete_multiply_dailynotes),
    path('dailynotes_service/update_dailynotes/', dailynotes_views.update_dailynotes),
    
    path('mail_service/send_password_mail/', mail_views.send_password_mail),
    path('mail_service/verify_reset_code/', mail_views.verify_reset_code),

    path('auth_service/reset_password/', auth_views.reset_password),
    path('auth_service/generate_refresh_token/', token_service.generate_refresh_token),
    path('auth_service/generate_access_token/',  token_service.generate_access_token),
    path('auth_service/verify_token/', token_service.verify_token),
    path('auth_service/get_current_user/', token_service.get_current_user),
    path('auth_service/refresh_access_token/', token_service.refresh_access_token),
    
    
]
