from django.urls import path
from . import views

urlpatterns = [
    # Student URLs
    path('', views.student_list, name='student_list'),
    # path('add/', views.student_add, name='student_add'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    # path('<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # Allocation URLs
    path('allocations/', views.allocation_list, name='allocation_list'),
    # path('allocations/add/', views.allocation_add, name='allocation_add'),
    path('allocations/<int:pk>/delete/', views.allocation_delete, name='allocation_delete'),
    
    # Student Profile URLs
    path('profile/edit/', views.student_profile_edit, name='student_profile_edit'),
]
