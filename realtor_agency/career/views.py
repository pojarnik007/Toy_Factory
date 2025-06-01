from django.shortcuts import render
from .models import Vacancy


def vacancies(request):
    vacs = Vacancy.objects.all()
    return render(request, 'career/vacancies.html', context={'vacancies': vacs})
