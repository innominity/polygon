from django.urls import path
from .views import app_main

urlpatterns = [
    path('app/<str:app_slug>/', app_main),
]
