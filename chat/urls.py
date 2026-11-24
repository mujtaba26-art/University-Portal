# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('get-messages/<int:user_id>/', views.get_messages, name='get_messages'),
    path('send-message/', views.send_message, name='send_message'),
]
