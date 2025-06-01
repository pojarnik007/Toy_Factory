from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('stats/', views.stats, name='stats'),
]
