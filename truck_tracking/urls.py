from django.urls import path
from . import views

urlpatterns = [
    path('', views.truck_list, name='truck_list'),
    path('create/', views.truck_create, name='truck_create'),
    path('update/<int:pk>/', views.truck_update, name='truck_update'),
    path('delete/<int:pk>/', views.truck_delete, name='truck_delete'),
    path('set-arrived/<int:pk>/', views.set_arrived_status, name='set_arrived_status'),
]