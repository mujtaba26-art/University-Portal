from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('',views.logins,name='login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('profile/', views.edit_teacher_profile, name='edit_profile'),

    path('upload_folder/<pk>/<subject>/',views.upload_folder,name='upload_folder'),
     path('edit_uploadfolder/<pk>/<subject>/',views.editupload_folder,name='edit_upload_folder'),

    path('preview_pdf/<str:subject>/',views.pdfsview,name='preview-pdf'),

    path('logout/',views.logouts,name='logouts'),
    
    path('chat/', views.chat_view, name='chat'),
    path('send/', views.send_message, name='send_message'),
    path('get-messages/', views.get_messages, name='get_messages'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users/', views.admin_users_list, name='admin_users'),
    path('admin-dashboard/users/create/', views.admin_create_user, name='admin_create_user'),
    path('admin-dashboard/academic/', views.admin_academic_management, name='admin_academic'),
    path('admin-dashboard/documents/', views.admin_document_management, name='admin_documents'),
    
    path('subject-data/',views.admin_subject_data_view, name='admin_subject_data'),

    
    path('clear-notifications/', views.clear_notifications, name='clear_notifications'),
    path('api/unread-message-count/', views.get_unread_message_count, name='unread_message_count'),


]



