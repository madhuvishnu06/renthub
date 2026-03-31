from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('<int:booking_id>/process/', views.payment_process, name='process'),
    path('<int:pk>/success/', views.payment_success, name='success'),
    path('<int:pk>/failed/', views.payment_failed, name='failed'),
    path('qr-code/', views.qr_code_manage, name='qr_code'),
    path('', views.payment_list, name='list'),
]
