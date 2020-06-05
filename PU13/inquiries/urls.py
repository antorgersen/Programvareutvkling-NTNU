from django.urls import path

from . import views

urlpatterns = [
    path("kontakt/", views.home, name ="kontakt")
]