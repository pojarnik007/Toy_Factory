from django.urls import path
from .views import *

app_name = 'production'

urlpatterns = [
    path('catalog/', catalog, name='catalog'),
    path('create/', create, name='create'),
    path('edit/<int:pk>/', toy_detail, name='edit'),
    path('delete/<int:pk>/', delete, name='delete'),
    path('orders/', order_list, name='orders'),   # <-- добавлено!
    path('detail/<int:pk>/', toy_detail_view, name='detail'),
    path('buy/<int:pk>/', buy, name='buy'),
    path('order_confirm/<int:order_id>/', order_confirm, name='order_confirm'),
    path('admin_order_confirm/<int:order_id>/', order_confirm_admin, name='admin_order_confirm'),
]