from django.test import TestCase, Client
from django.urls import reverse, resolve

from .views import home

from .forms import SendMessageToAdmin
from .models import Inquiries





class TestInquiries(TestCase):
    # Runs before all tests
    def setUp(self):
        self.client = Client()
        self.url = reverse("kontakt")
        #lager en fiktiv melding
        self.melding1 = Inquiries.objects.create(
            text_from="hejek",
            subject="hejk",
            description="hjklkjh",
            created_at=0
        )
    # Tester om urlen faktisk gir deg riktig view
    def test_kontakt_url_resolves(self):

        self.assertEquals(resolve(self.url).func, home)

    # Tester det å fylle ut skjemaet
    def test_inquiries_home_POST_add_new_message(self):
        response = self.client.post(self.url, {
            "text_from": "hejek",
            "subject": "hejk",
            "description": "hjklkjh",
            "created_at": "0"
        })

        self.assertEquals(self.melding1.text_from, "hejek")

        self.assertEquals(response.status_code, 302)

    # Under vises metoden for å teste get-request. Å hente ned siden. I tillegg at riktig template er brukt.
    def test_GET_request_and_correct_template(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "contact_admin.html")



    # Tester at det er mulig å legge til gyldig data
    def test_valid_data(self):
        form = SendMessageToAdmin(data={
            "text_from": "Andreas",
            "subject": "Trenger hjelp med å legge ut annonse",
            "description": "Når jeg logger inn så får jeg masse feil med bla bla bla."
        }

        )
        self.assertTrue(form.is_valid())
    # Tester at det ikke er mulig å legge til ugyldig data
    def test_invalid_data(self):
        form = SendMessageToAdmin(data={

        })
        self.assertFalse(form.is_valid())

        #Sjekker at antall feil i skjemaet er 3.
        self.assertEquals(len(form.errors), 3)
