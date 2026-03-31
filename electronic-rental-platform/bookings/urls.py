from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:product_id>/', views.booking_create, name='create'),
    path('<int:pk>/invoice/', views.booking_invoice, name='invoice'),
    path('', views.booking_list, name='list'),
    path('<int:pk>/', views.booking_detail, name='detail'),
    path('<int:pk>/cancel/', views.booking_cancel, name='cancel'),
    path('<int:pk>/approve/', views.booking_approve, name='approve'),
    path('<int:pk>/reject/', views.booking_reject, name='reject'),
    path('<int:pk>/confirm/', views.booking_confirm, name='confirm'),
    path('<int:pk>/complete/', views.booking_complete, name='complete'),
]
