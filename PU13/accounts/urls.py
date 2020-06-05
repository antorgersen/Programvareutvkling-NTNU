from django.urls import path
from .views import SignUpView

# Viser hvilken link som tilhører views, kun linkene relatert til registrering og logg inn
urlpatterns = [
    path('registrer/', SignUpView.as_view(), name='signup'),
]