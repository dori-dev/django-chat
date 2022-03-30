"""chat urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.index, name='index'),
    path('groups/', views.group_list, name="groups"),
    path('create/', views.create_group, name='create'),
    path('chat/<str:room_name>/', views.room, name='room'),
]
