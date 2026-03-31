from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.conversation_detail, name='conversation'),
    path('start/<int:user_id>/', views.start_conversation, name='start'),
    path('<int:pk>/delete/', views.delete_conversation, name='delete'),
]
