from django.urls import path, re_path
from .views import *

app_name = 'filling'

urlpatterns = [
    path('index/', index, name='index'),
    path('about/', about, name='about'),
    re_path(r'^article/(?P<slug>[\w-]+)/$', article_detail, name='article'),
    path('news/', article_list, name='news'),
    path('faq/', faq, name='faq'),
    path('conf_politic/', conf_politic, name='conf_politic'),
    path('catfact/', random_cat_fact, name='random_cat_fact'),
    path('dog/', random_dog_image, name='random_dog_image'),
]