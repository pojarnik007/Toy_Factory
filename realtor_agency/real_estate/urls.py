from django.urls import path, re_path
from .views import *

app_name = 'real_estate'

urlpatterns = [
    path('catalog/', catalog, name='catalog'),
    path('create/', create, name='create'),
    re_path(r'edit/(?P<slug>[\w-]+)/$', real_estate_detail, name='edit'),
    re_path(r'delete/(?P<slug>[\w-]+)/$', delete, name='delete'),
    re_path(r'detail/(?P<slug>[\w-]+)/$', detail, name='detail'),
    re_path(r'buy/(?P<slug>[\w-]+)/$', buy, name='buy'),
    path('sales/', sales, name='sales'),
]