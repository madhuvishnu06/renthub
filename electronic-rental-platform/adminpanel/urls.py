from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.manage_users, name='users'),
    path('products/', views.manage_products, name='products'),
    path('bookings/', views.manage_bookings, name='bookings'),
    path('categories/', views.manage_categories, name='categories'),
]
