"""core URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),
    path('chat/', include('chat.urls')),
    path('auth/', include('auth.urls')),
]
