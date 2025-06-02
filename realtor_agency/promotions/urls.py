from django.urls import path
from .views import promocodes, promocode_add, promocode_delete

app_name = 'promotions'

urlpatterns = [
    path('promocodes/', promocodes, name='promocodes'),
    path('promocodes/add/', promocode_add, name='promocode_add'),
    path('promocodes/delete/<int:pk>/', promocode_delete, name='promocode_delete'),
]