from django.urls import path
from . import views

app_name = 'returns'

urlpatterns = [
    # Return request URLs
    path('request/create/<int:booking_id>/', views.return_request_create, name='request_create'),
    path('request/<int:pk>/', views.return_request_detail, name='request_detail'),
    path('request/<int:pk>/review/', views.return_request_review, name='request_review'),
    path('requests/', views.return_request_list, name='request_list'),
    
    # Notification URLs
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:pk>/mark-as-read/', views.notification_mark_as_read, name='notification_mark_as_read'),
    path('notifications/<int:pk>/delete/', views.notification_delete, name='notification_delete'),
    path('api/notifications/unread/', views.get_unread_notifications, name='api_unread_notifications'),
]
