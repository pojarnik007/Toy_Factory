from django.urls import path
from . import views

app_name = 'career'

urlpatterns = [
    path('vacancies/', views.vacancies, name='vacancies'),
    path("vacancy/<int:pk>/", views.vacancy_detail, name="vacancy_detail"),  # 👈 добавляем
    path("vacancy/<int:pk>/apply/", views.apply, name="apply"),
]