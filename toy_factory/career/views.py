from django.shortcuts import render, get_object_or_404
from .models import Vacancy

def vacancies(request):
    vacancies = Vacancy.objects.all()
    return render(request, "career/vacancies.html", {"vacancies": vacancies})

def vacancy_detail(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    return render(request, "career/vacancy_detail.html", {"vacancy": vacancy})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Vacancy

def apply(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)

    if request.method == "POST":
        # Тут можно сохранить отклик в базу (например, VacancyApplication)
        # Сейчас просто заглушка
        return redirect("career:vacancies")

    return render(request, "career/apply.html", {"vacancy": vacancy})
