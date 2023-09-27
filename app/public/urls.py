from django.urls import path

from app.public.views import home

urlpatterns = [
    path("", home, name="home"),
]
