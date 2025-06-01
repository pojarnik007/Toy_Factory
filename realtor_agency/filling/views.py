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


def knock_knock_joke(request):
    url = "https://official-joke-api.appspot.com/jokes/knock-knock/random"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        joke_data = response.json()[0]
        context = {
            'setup': joke_data['setup'],
            'punchline': joke_data['punchline']
        }
    except Exception as e:
        context = {
            'error': f"Не удалось загрузить шутку: {str(e)}"
        }
    
    return render(request, 'filling/joke.html', context)


def random_quote(request):
    url = "https://favqs.com/api/qotd"
    
    try:
        response = requests.get(url, timeout=5, 
            headers={'Authorization': 'Authorization: Token token="15d75e69a9b659eab0cb45caeeb098ac"'})
        
        response.raise_for_status()
        data = response.json()
        quote_data = data['quote']
        context = {
            'body': quote_data['body'],
            'author': quote_data['author']
        }
    except Exception as e:
        context = {
            'error': f"Не удалось загрузить шутку: {str(e)}"
        }
    
    return render(request, 'filling/quotes.html', context)


def page_not_found(request, exception):
    return render(request, 'page_not_found.html')