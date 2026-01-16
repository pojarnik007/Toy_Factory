from django.http.response import HttpResponse, HttpResponseNotFound

def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    if article:
        return render(request, 'filling/article.html', context={'article': article})
    else:
        return HttpResponseNotFound()

def article_list(request):
    article_list = Article.objects.all()
    return render(request, 'filling/article_list.html', context={'article_list': article_list})


def faq(request):
    question_and_answers = FAQ.objects.all()
    return render(request, 'filling/faq.html', context={'question_and_answers': question_and_answers})



def conf_politic(request):
    return render(request, 'filling/conf_politic.html')


import requests
from django.shortcuts import render

def random_cat_fact(request):
    url = "https://catfact.ninja/fact"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        fact_data = response.json()
        context = {
            'setup': "Факт о кошках:",
            'punchline': fact_data.get('fact', 'Нет данных.')
        }
    except Exception as e:
        context = {
            'error': f"Не удалось загрузить факт: {str(e)}"
        }
    return render(request, 'filling/cta_fact.html', context)

import requests
from django.shortcuts import render

def random_dog_image(request):
    url = "https://dog.ceo/api/breeds/image/random"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        context = {
            'setup': "Случайная собака дня:",
            'punchline': "",  # картинка будет ниже
            'dog_image': data.get('message')
        }
    except Exception as e:
        context = {
            'error': f"Не удалось получить изображение собаки: {str(e)}"
        }
    return render(request, 'filling/dog.html', context)


def page_not_found(request, exception):
    return render(request, 'page_not_found.html')


# filling/views.py

from django.shortcuts import render
from .models import CompanyInformation, CompanyHistory, Partner, Article, FAQ

def about(request):
    company_info = CompanyInformation.objects.first()
    history_events = CompanyHistory.objects.all()

    # === ДОБАВЛЯЕМ ЭТУ СТРОКУ ===
    partners_list = Partner.objects.all()

    context = {
        'info': company_info,
        'history': history_events,
        'partners': partners_list,  # <-- И передаем в контекст
    }
    return render(request, 'filling/about.html', context)


# ... остальной код views.py ...

# --- Остальные представления остаются без изменений ---

# filling/views.py
from .models import Article, PromoSlide, SliderSettings  # Не забудьте импортировать новые модели


def index(request):
    latest_articles = Article.objects.all()[:3]
    slides = PromoSlide.objects.all()

    settings, created = SliderSettings.objects.get_or_create(
        id=1,  # синглтон
        defaults={'delay': 5000, 'is_auto': True, 'is_loop': True}
    )

    context = {
        'latest_articles': latest_articles,
        'slides': slides,
        'slider_settings': settings,
    }
    return render(request, 'filling/index.html', context)
# ... и так далее

def all_examples(request):
    return render(request, 'filling/all_types.html')

