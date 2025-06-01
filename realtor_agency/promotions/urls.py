from django.urls import path
from .views import promocodes

app_name = 'promotions'

urlpatterns = [
    path('promocodes/', promocodes, name='promocodes')
]