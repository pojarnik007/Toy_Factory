from django.contrib.auth.views import LogoutView
from django.urls import include, path, re_path
from .views import *

app_name = 'users'

urlpatterns = [
    
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/<str:name>/', user_profile, name='user_profile'),
]
