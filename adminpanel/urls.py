from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    # path('',views.logins,name='login'),
    path('',views.adminpanel,name='adminpanel'),
    path('createuser/',views.create_user_view,name='createusers'),
    path('user/',views.user_list_view,name='users'),
    path('edituser/<int:user_id>/',views.edit_user,name='edit_user'),
    # path('teacherdocument/<user>/<subject>/',views.teachersdocumentviews,name='teacher_document')
    # path('profile/', views.edit_teacher_profile, name='edit_profile'),
    path("get-messages/", views.get_messages, name="get_messages"),
    path("send-message/", views.send_message, name="send_message"),
    
    # path('logout/',views.logouts,name='logouts')
]

