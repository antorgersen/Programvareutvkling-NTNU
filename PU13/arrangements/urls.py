from django.urls import path
from . import views

urlpatterns = [
    # Link for challenge views
    path("utfordring/", views.challengeView, name="chall"),
    path("utfordring/<int:pk>/", views.challenge_detail, name="challenge_detail"),
    path("utfordring/opprett/", views.create_challenge, name="create_challenge"),

    # Link for knit views
    path("strikkekveld/", views.knitView, name="knit"),
    path("strikkekveld/opprett/", views.create_knit, name="create_knit"),
    path("strikkekveld/<int:pk>/", views.knit_detail, name="knit_detail"),

    # Link for knit views
    path("annonse/", views.yarnView, name="yarn"),
    path("annonse/opprett/", views.create_yarn, name="create_yarn"),
    # path("annonse/<int:pk>/", views.knit_detail, name="knit_detail"),

    # Link for my page
    path("minside/", views.my_page, name="my_page"),
    path("minside/avmeld/utfordring/<int:pk>/", views.deregister_challenge, name="delete"),
    path("minside/avmeld/strikkekveld/<int:pk>/", views.deregister_knit, name="delete_knit"),
    path("minside/fullfort/utfordring", views.complete_challenge, name="complete"),
]
