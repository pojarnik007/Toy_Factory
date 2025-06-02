from django.shortcuts import redirect, render
from django.http.response import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from .models import FAQ, Article, CompanyInformation
import requests

def index(request):
    article = Article.objects.all().first()
    return render(request, 'filling/article.html', context={'article': article})


def about(request):
    info = CompanyInformation.objects.all().first()
    return render(request, 'filling/about.html', context={'info': info})


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