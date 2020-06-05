import unittest

from .views import personal_feed_view, create_blog_view, detail_blog_view
from .forms import Create_Personal_Feed_Post_Form
from .models import Personal_Feed_Post
import os
from os import path
import sys
from django.contrib.messages import get_messages

sys.path.append('..')
from django.test import TestCase, Client
from accounts.models import CustomUser

# Create your tests here.
from django.urls import resolve, reverse

print(os.getcwd())


# Start off with setting up before each test


class TestPersonalFeed(TestCase):
    @classmethod
    def setUp(self):
        self.client = Client()
        self.my_user = CustomUser.objects.create_user(username='test123', password='test123', name='AAron')
        self.feed_url = reverse('personal_feed:personal_feed')
        self.create_url = reverse('personal_feed:create')
        self.detail_url = reverse('personal_feed:detail', args=[1])

    # Making sure we can send in a form successfully

    def test_valid_form(self):
        post_form = {
            'title': 'Testing',
            'content': 'Testing again',
        }
        form = Create_Personal_Feed_Post_Form(data=post_form)
        print(form.errors)
        self.assertTrue(form.is_valid())

    # Testing if we're correctly redirected when we submit form

    def test_redirect(self):
        login = self.client.login(username='test123', password='test123')
        self.assertTrue(login)

        response = self.client.post(self.create_url, {

            "title": "Heisann",
            "content": "Heiheihei",
            "author": self.my_user,
            'slug': 'django'
        }
                                    )

        self.assertEquals(response.status_code, 302)

    # Checking our views and templates

    def test_views_and_templates(self):
        login = self.client.login(username='test123', password='test123')
        self.assertTrue(login)

        response = self.client.get(self.feed_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "personal_feed.html")

        second_response = self.client.get(self.create_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(second_response, "create_blog.html")

    # Checking to make sure our reponse message is correct
    def test_response_message(self):
        login = self.client.login(username='test123', password='test123')
        self.assertTrue(login)
        response = self.client.post(self.create_url, {

            "title": "Heisann",
            "content": "Heiheihei",
            "author": self.my_user,
            'slug': 'django'
        }
                                    )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Innlegget er blitt lagt ut')

    # Testing for invalid input

    def test_invalid_input(self):
        form =  {
            "title": "",
            "content": "",
        }

        form = Create_Personal_Feed_Post_Form(data=form)
        self.assertFalse((form.is_valid()))

