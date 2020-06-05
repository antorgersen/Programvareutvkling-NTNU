from urllib import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import MyUserCreationForm
from django.contrib.messages.views import SuccessMessageMixin


# Logikken bak registreringsskjemaet, bruker innebygd Django generic createview
class SignUpView(SuccessMessageMixin, CreateView):
    """SuccessMessageMixin støtter class-based-views til å håndtere suksessmeldinger på vellykde forms.
       Bruker variabelen 'sucess_message' til å skrive ut meldingen. """

    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    success_message = "%(username)s er registrert!"
    template_name = 'registration/signup.html'
