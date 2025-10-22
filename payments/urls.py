from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('add/', views.payment_add, name='payment_add'),
    path('<int:pk>/', views.payment_detail, name='payment_detail'),
    path('<int:pk>/edit/', views.payment_edit, name='payment_edit'),
    path('<int:pk>/update-status/', views.payment_update_status, name='payment_update_status'),
    path('<int:pk>/delete/', views.payment_delete, name='payment_delete'),
    path('make/', views.student_payment_make, name='student_payment_make'),
]
