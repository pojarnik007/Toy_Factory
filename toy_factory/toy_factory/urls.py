from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('filling/', include('filling.urls'), name='filling'),
    path('users/', include('users.urls'), name='users'),
    path('reviews/', include('reviews.urls'), name='reviews'),
    path('contacts/', include('contacts.urls'), name='contacts'),
    path('promotions/', include('promotions.urls'), name='promotions'),
    path('career/', include('career.urls'), name='career'),
    path('statistic/', include('statistic.urls'), name='statistic'),
    path('production/', include('production.urls'), name='toys'),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

