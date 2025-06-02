
from .views import vacancies
from django.urls import path

app_name = 'career'

urlpatterns = [
    path('vacancies/', vacancies, name='vacancies'),
]