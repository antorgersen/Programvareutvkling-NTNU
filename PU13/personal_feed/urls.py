from django.urls import path

from .views import personal_feed_view, create_blog_view, detail_blog_view
from arrangements.views import *

app_name = 'personal_feed'

urlpatterns = [
    path("personal_feed/", personal_feed_view, name="personal_feed"),
    path("create/", create_blog_view, name="create"),
    path("<slug>/", detail_blog_view, name="detail"),
]
