from django.shortcuts import render

# Create your views here.
from .forms import SendMessageToAdmin
from .models import Inquiries

from django.shortcuts import render, redirect
#from django.http import HttpResponse, HttpResponseRedirect
#from django.urls import reverse

from django.contrib import messages

def home(response):
    if response.method == "POST":
        form = SendMessageToAdmin(response.POST)
        if form.is_valid():
            a = form.cleaned_data["text_from"]
            t = form.cleaned_data["subject"]
            d = form.cleaned_data["description"]
            f = Inquiries(text_from=a, subject=t, description=d)
            f.save()
            messages.success(response, 'Melding sendt!')

            response = redirect('kontakt')
            return response
        else:
            messages.error(response, 'Fyll ut alle feltene!!')

    else:
        form = SendMessageToAdmin()

    return render(response, "contact_admin.html", {"form": form})
