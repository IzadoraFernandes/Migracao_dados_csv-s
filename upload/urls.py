from django.urls import path
from .views import *

urlpatterns = [
    path('ratings/', rating_list, name='rating_list'),
    path('ratings/new/', rating_create, name='rating_create'),
    path('ratings/edit/<int:pk>/', rating_update, name='rating_update'),
    path('ratings/delete/<int:pk>/', rating_delete, name='rating_delete'),
    
    path('tags/', tag_list, name='tag_list'),
    path('tags/new/', tag_create, name='tag_create'),
    path('tags/edit/<int:pk>/', tag_update, name='tag_update'),
    path('tags/delete/<int:pk>/', tag_delete, name='tag_delete'),
    
    path('upload_csv/', upload_csv, name='upload_csv'),
    path('upload_success/', upload_success, name='success'),
]
