from django.urls import path
from . import views

# ВАЖНО: Эта строка регистрирует namespace
app_name = 'contacts'

urlpatterns = [
    # name='contacts' означает, что ссылка будет contacts:contacts
    path('', views.contacts, name='contacts'),
    path('json/', views.get_contacts_json, name='contacts_json'),
]