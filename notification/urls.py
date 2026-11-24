from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    
        path('notifications/', views.fetch_notifications, name='fetch_notifications'),
    

    
]



