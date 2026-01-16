# filling/urls.py

from django.urls import path, re_path
# Явный импорт всех представлений вместо "*"
from .views import (
    index, 
    about, 
    article_detail, 
    article_list, 
    faq, 
    conf_politic, 
    random_cat_fact, 
    random_dog_image,
    all_examples
)

app_name = 'filling'

urlpatterns = [
    path('index/', index, name='index'),
    path('about/', about, name='about'),
    # Эта строка теперь должна работать без ошибок
    re_path(r'^article/(?P<slug>[\w-]+)/$', article_detail, name='article'),
    path('news/', article_list, name='news'),
    path('faq/', faq, name='faq'),
    path('conf_politic/', conf_politic, name='conf_politic'),
    path('catfact/', random_cat_fact, name='random_cat_fact'),
    path('dog/', random_dog_image, name='random_dog_image'),
    path('all/', all_examples, name='all_examples'),
]