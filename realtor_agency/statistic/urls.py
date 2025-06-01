# urls.py
from django.urls import path
from .views import statistics_view

app_name = 'statistic'

urlpatterns = [
    path("", statistics_view, name="statistic"),
]
