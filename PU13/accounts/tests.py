import unittest

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import MyUserCreationForm
from .models import CustomUser


class AccountsTesting(TestCase):
    @classmethod
    def setUp(self):
        # This creates a user that is used to simulate tests
        CustomUser.objects.create_user(username='test123', password='test123', name='AAron')
        # Here we're giving ourselves a shortcut to refer back to other URLs
        self.login_success_URL = reverse("home")
        self.registration_URL = reverse("accounts:signup")

    def test_Login(self):
        # First we check if we can log in with the user we created
        self.assertTrue(self.client.login(username="test123", password="test123"))

        # Checking to see if we're being redirected to the correct template upon successful login
        response = self.client.get(self.login_success_URL)
        # When you successfully reach a website, the status code will be 200 (as opposed to 404: Not Found)
        self.assertEquals(response.status_code, 200)
        # Checking to make sure we've been redirected to the home page
        self.assertTemplateUsed(response, "home.html")

    def test_register_new_user(self):
        # self.assertFalse(self.client.login(username='ronzay_5', password='ronzay666'))
        # Essentially filling out a form to send for registration
        # Create a dictionary with necessary fields to send to our form
        form_data = {
            'username': 'itsronzayyall',
            'name': 'Ronzay',
            'user_level': 'Nybegynner',
            'password1': 'ronzay666',
            'password2': 'ronzay666'

        }

        # We enter the above information into our form (MyUserCreationForm) and define it as a variable
        form = MyUserCreationForm(data=form_data)
        # IMPORTANT TOOL!! This is how you can look for errors to correct, otherwise you don't get detailed feedback
        # on what's failing
        print(form.errors)
        # Checking to see if our form with the defined input is valid
        self.assertTrue(form.is_valid())
        response = self.client.post(self.registration_URL, form_data)
        self.assertEqual(response.status_code, 302)
        # Then, we check to see if we can log in with our new registered user
        self.assertTrue(self.client.login(username='itsronzayyall', password='ronzay666'))

    def test_inValid_Password_Registration(self):
        form_data = {
            'username': 'itsronzayyall',
            'name': 'Ronzay',
            'user_level': 'Nybegynner',
            'password1': 'ronzay666',
            'password2': 'ronzay66'

        }

        form = MyUserCreationForm(data=form_data)

        # Through having used form.errors, I found that the error message posted for an unmatching
        # password would be as following, so I ran my test through making two mismatched passwords and
        # checking to see if we got the according error message, which we did/do

        self.assertEquals({'password2': ['The two password fields didn’t match.']}, form.errors)

    # Trying a new method, here we have isolated that the password is the only error, seeing as the form
    # was valid above and this is our only change. assertEquals could not be used here, so a better current
    # solution is to check for an expected error.
    @unittest.expectedFailure
    def test_inValid_Password(self):
        form_data = {
            'username': 'itsronzayyall',
            'name': 'Ronzay',
            'user_level': 'Nybegynner',
            'password1': 'ronzay6',
            'password2': 'ronzay6'

        }

        form = MyUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_Valid_Name(self):
        # In the last test, we're checking the last input field that can be manually incorrect, the name.
        # This will be harder to test when character limits pass a certain level, but for now, we enter a
        # name with over 20 characters, knowing that we have a lower limit, and then check to see if we
        # get the correct error message
        form_data = {
            'username': 'itsronzayyall',
            'name': 'Ronzayyyyyyyyyyyyyyyyyyyyy',
            'user_level': 'Nybegynner',
            'password1': 'ronzay666',
            'password2': 'ronzay666'

        }

        form = MyUserCreationForm(data=form_data)
        print(form.errors)

        self.assertEquals({'name': ['Ensure this value has at most 20 characters (it has 26).']}, form.errors)
