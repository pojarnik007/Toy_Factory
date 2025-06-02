from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('', index, name='index'),
    path('create/', create, name='create'),
    path('edit/<int:id>/', edit, name='edit'),
    path('delete/<int:id>/', delete, name='delete'),
]