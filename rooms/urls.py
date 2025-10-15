from django.urls import path
from . import views

urlpatterns = [
    # Room URLs
    path('', views.room_list, name='room_list'),
    path('add/', views.room_add, name='room_add'),
    path('<int:pk>/', views.room_detail, name='room_detail'),
    path('<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('<int:pk>/delete/', views.room_delete, name='room_delete'),
    
    # Hostel URLs
    path('hostels/', views.hostel_list, name='hostel_list'),
    path('hostels/add/', views.hostel_add, name='hostel_add'),
    path('hostels/<int:pk>/', views.hostel_detail, name='hostel_detail'),
    path('hostels/<int:pk>/edit/', views.hostel_edit, name='hostel_edit'),
    path('hostels/<int:pk>/delete/', views.hostel_delete, name='hostel_delete'),
]
