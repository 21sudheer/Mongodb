from django import urls
from django.urls import path
from . import views

urlpatterns = [
    path("", views.Ajax_view, name="Ajax_view"),
]
