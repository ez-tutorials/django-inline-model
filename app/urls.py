from django.conf.urls import url
from django.urls import path

from .views import countries_view


urlpatterns = [
    path('', countries_view, name='country_new'),
]
