from django.urls import path
from .views import *
from . import views

app_name = 'production'

urlpatterns = [
    path('catalog/', catalog, name='catalog'),
    path('create/', create, name='create'),
    path('edit/<int:pk>/', toy_detail, name='edit'),
    path('delete/<int:pk>/', delete, name='delete'),
    path('orders/', order_list, name='orders'),
    path('detail/<int:pk>/', toy_detail_view, name='detail'),
    path('buy/<int:pk>/', buy, name='buy'),
    path('order_confirm/<int:order_id>/', order_confirm, name='order_confirm'),
    path('admin_order_confirm/<int:order_id>/', order_confirm_admin, name='admin_order_confirm'),
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add/<int:toy_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/<str:action>/", views.update_cart_item, name="update_cart_item"),
    path("cart/checkout/", views.checkout, name="checkout"),
]