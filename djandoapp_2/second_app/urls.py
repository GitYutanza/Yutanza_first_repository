# myapp/urls.py
from django.urls import path

from .views import *

urlpatterns = [
    path('', user_form_view, name='user_form'),
    path('success/', success_view, name='success'),
    path('pay/', PayView.as_view(), name="app")
]
