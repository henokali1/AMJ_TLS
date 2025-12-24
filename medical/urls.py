from django.urls import path
from . import views

urlpatterns = [
    path('', views.ClientListView.as_view(), name='client_list'),
    path('new/', views.ClientCreateView.as_view(), name='client_create'),
    path('<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_update'),
    path('<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    
    # Template URLs
    path('templates/', views.TemplateListView.as_view(), name='template_list'),
    path('templates/new/', views.TemplateCreateView.as_view(), name='template_create'),
    path('templates/<int:pk>/edit/', views.TemplateUpdateView.as_view(), name='template_update'),
    path('templates/<int:pk>/delete/', views.TemplateDeleteView.as_view(), name='template_delete'),
    path('templates/<int:pk>/finder/', views.CoordinateFinderView.as_view(), name='coordinate_finder'),
    path('client/<int:client_pk>/certificate/', views.view_certificate, name='view_certificate'),
    
    # User Management
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/new/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_update'),
]
