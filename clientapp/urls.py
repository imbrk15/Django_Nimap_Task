
from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.list_clients, name='list_clients'),
    path('clients/', views.create_client, name='create_client'),
    path('clients/<int:pk>/', views.retrieve_client, name='retrieve_client'),
    path('clients/<int:pk>/', views.update_client, name='update_client'),
    path('clients/<int:pk>/', views.delete_client, name='delete_client'),
    path('clients/<int:client_id>/projects/',
         views.create_project, name='create_project'),
    path('projects/', views.list_user_projects, name='list_user_projects'),
]
