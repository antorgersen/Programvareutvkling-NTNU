from datetime import time, date, datetime
from django.utils import timezone
from django.test import TestCase, Client
import sys
import pytz

from accounts.models import CustomUser

sys.path.append('..')
# Create your tests here.
from django.urls import resolve, reverse
from .views import challengeView, knitView, my_page, create_knit, create_challenge, complete_challenge, \
    challenge_detail, knit_detail, deregister_challenge, deregister_knit, yarnView, create_yarn
from .forms import CreateChallenge, CreateKnit, CreateYarn
from .models import Challenge, KnitNight, Ads
import os

print(os.getcwd())


# Tester for utfordringer


class TestChallengeUrl(TestCase):
    def setUp(self):
        # Ser her at vi kan bruke to måter å skrive urlen på
        self.utfordring_url = "/utfordring/"  # reverse("chall")
        self.utfordring_opprett_url = reverse("create_challenge")
        # Må legge til argumenter for å at urlen skal finnes
        self.utfordring_detaljer_url = reverse("challenge_detail", args=[123])

    def test_url(self):
        self.assertEquals(resolve(self.utfordring_url).func, challengeView)
        self.assertEquals(resolve(self.utfordring_opprett_url).func, create_challenge)
        self.assertEquals(resolve(self.utfordring_detaljer_url).func, challenge_detail)


class TestChallengeViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.chall_url = reverse("chall")
        self.utfordring_opprett_url = reverse("create_challenge")
        self.chall_detail_url = reverse("challenge_detail", args=[1])
        self.user1 = CustomUser.objects.create_user(username='test123', password='test123', name='AAron')
        self.user2 = CustomUser.objects.create_user(username='test1234', password='test1234', name='AAron1')
        self.challenge1 = Challenge.objects.create(
            challenge_name="Hansker",
            description="Hansker med avtagbare fingre",
            rec_user_level="Legende",
            created_at=date(2020, 4, 12),
            created_by=self.user1,
        )
        login = self.client.login(username='test123', password='test123')

        self.assertTrue(login)

    def test_challenge_view(self):
        response = self.client.get(self.chall_url)
        # Sjekker om den klarer å hente ned siden (HTTP-response code 200)
        self.assertEquals(response.status_code, 200)
        # Sjekker om den bruker riktig template
        self.assertTemplateUsed(response, "challenge/challenge.html")

    def test_challenge_details_get(self):
        response = self.client.get(self.chall_detail_url)
        # Sjekker om den klarer å hente ned siden (HTTP-response code 200)
        self.assertEquals(response.status_code, 200)
        # Sjekker om den bruker riktig template
        self.assertTemplateUsed((response, "challenge/challenge_detail.html"))

    def test_challenge_details_post(self):
        # Melder på bruker 1
        response = self.client.post(self.chall_detail_url)
        # Logger ut bruker 1
        self.client.logout()
        # Logger inn bruker 2
        self.client.login(username="test1234", password="test1234")
        # melder på bruker 2
        self.client.post(self.chall_detail_url)
        # Sjekker response-kode
        self.assertEquals(response.status_code, 200)
        # Sjekker at det er 2 påmeldte.
        self.assertEquals(Challenge.objects.all()[0].participants.count(), 2)

    def test_create_challenge(self):
        # Lager et objekt i databasen
        response = self.client.post(self.utfordring_opprett_url, {

            "challenge_name": "Heisann",
            "description": "Heiheihei",
            "rec_user_level": "Legende"}
                                    )
        # Sjekker at det er riktig http-response kode (302 fordi man blir redirectet til en annen url)
        self.assertEquals(response.status_code, 302)
        # Sjekker at det andre objektet har navnet "Heisann" (Første objektet er det som blir laget i
        self.assertEquals(Challenge.objects.all()[1].challenge_name, "Heisann")

    def test_create_no_challenge(self):
        response = self.client.post(self.utfordring_opprett_url)
        # Sjekker at det er riktig http-response kode (200 fordi man blir på samme side denne gangen)
        self.assertEquals(response.status_code, 200)
        # Sjekker at det andre objektet har navnet "Heisann" (Første objektet er det som blir laget i setUp-metoden)
        self.assertEquals(Challenge.objects.all().count(), 1)


# Tester for selve skjemaet
class TestChallangeForm(TestCase):
    def test_valid_data(self):
        form = CreateChallenge(data={
            "challenge_name": "Verdens lengste skjerf",
            "rec_user_level": "Legende",
            "description": "Du må lage et skjerf på mer enn 5 kilometer for å slå rekorden"

        }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = CreateChallenge(data={
            "challenge_name": "",
            "rec_user_level": "",
            "description": ""
        })
        self.assertFalse((form.is_valid()))


# Tester for strikkekveld
class TestKnitNightUrl(TestCase):
    def setUp(self):
        self.strikkekveld_url = reverse("knit")
        self.strikkekveld_opprett_url = reverse("create_knit")
        # Må legge til argumenter for å at urlen skal finnes
        self.strikkekveld_detaljer_url = reverse("knit_detail", args=[4])

    def test_url(self):
        self.assertEquals(resolve(self.strikkekveld_url).func, knitView)
        self.assertEquals(resolve(self.strikkekveld_opprett_url).func, create_knit)
        self.assertEquals(resolve(self.strikkekveld_detaljer_url).func, knit_detail)


# Tester for selve skjemaet

class TestKnitForm(TestCase):
    def test_valid_data(self):
        form = CreateKnit(data={
            "knit_name": "Star Wars strikkemaraton",
            "time": date(2020, 3, 23),
            "time_start": time(19, 30, 0),
            "description": "Vi skal se alle Star Wars-filmene mens vi strikker Star Wars-figurer. Bli med, dette blir "
                           "kjempegøy!"
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = CreateKnit(data={

        })
        self.assertFalse(form.is_valid())


class TestKnitViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.knit_url = reverse("knit")
        self.create_knit_url = reverse("create_knit")
        self.knit_detail = reverse("knit_detail", args=[1])
        self.user1 = CustomUser.objects.create_user(username='test123', password='test123', name='AAron')
        self.user2 = CustomUser.objects.create_user(username='test1234', password='test1234', name='AAron1')
        self.knit1 = KnitNight.objects.create(
            knit_name="StarWars strikkekveld",
            description="Masse gøy starwars-strikking",
            time=datetime(2020, 4, 20, tzinfo=pytz.UTC),
            time_start=time(19, 30, 0),
            created_at=timezone.now(),
            created_by=self.user1

        )
        login = self.client.login(username='test123', password='test123')

        self.assertTrue(login)

    def test_knit_view(self):
        response = self.client.get(self.knit_url)
        # Sjekker om den klarer å hente ned siden (HTTP-response code 200)
        self.assertEquals(response.status_code, 200)
        # Sjekker om den bruker riktig template
        self.assertTemplateUsed(response, "knit/knit.html")

    def test_knit_details_get(self):
        response = self.client.get(self.knit_detail)
        # Sjekker om den klarer å hente ned siden (HTTP-response code 200)
        self.assertEquals(response.status_code, 200)
        # Sjekker om den bruker riktig template
        self.assertTemplateUsed((response, "knit/knit_detail.html"))

    def test_knit_details_post(self):
        # Melder på bruker 1
        response = self.client.post(self.knit_detail)
        # Logger ut bruker 1
        self.client.logout()
        # Logger inn bruker 2
        self.client.login(username="test1234", password="test1234")
        # melder på bruker 2
        self.client.post(self.knit_detail)
        # Sjekker response-kode
        self.assertEquals(response.status_code, 200)
        # Sjekker at det er 2 påmeldte.
        self.assertEquals(KnitNight.objects.first().participants.count(), 2)

    def test_create_knit(self):
        # Lager et objekt i databasen
        response = self.client.post(self.create_knit_url, {

            "knit_name": "Heisannsveisann",
            "description": "Skikkelig bra strikkekveld kommer",
            "time": date(2020, 4, 21),
            "time_start": time(19, 30, 00),
        }
                                    )
        # Sjekker at det er riktig http-response kode (302 fordi man blir redirectet til en annen url)
        self.assertEquals(response.status_code, 302)
        # Sjekker at det andre objektet har navnet "Heisann" (Første objektet er det som blir laget i setUp-metoden)
        self.assertEquals(KnitNight.objects.all()[1].description, "Skikkelig bra strikkekveld kommer")

    def test_create_no_knit(self):
        response = self.client.post(self.create_knit_url)
        # Sjekker at det er riktig http-response kode (200 fordi man blir på samme side denne gangen)
        self.assertEquals(response.status_code, 200)
        # Sjekker at det andre objektet har navnet "Heisann" (Første objektet er det som blir laget i setUp-metoden)
        self.assertEquals(KnitNight.objects.all().count(), 1)


# Tester for min side
class TestMyPageUrl(TestCase):
    def setUp(self):
        self.min_side_url = reverse("my_page")
        self.min_side_fullført_utfordring_url = reverse("complete")
        # Må legge til argumenter for å at urlen skal finnes
        self.min_side_avmeld_utfordring_url = reverse("delete", args=[12])
        self.min_side_avmeld_strikkekveld_url = reverse("delete_knit", args=[2])

    def test_url(self):
        self.assertEquals(resolve(self.min_side_url).func, my_page)
        self.assertEquals(resolve(self.min_side_fullført_utfordring_url).func, complete_challenge)
        self.assertEquals(resolve(self.min_side_avmeld_utfordring_url).func, deregister_challenge)
        self.assertEquals(resolve(self.min_side_avmeld_strikkekveld_url).func, deregister_knit)


class TestMyPageViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.min_side_url = reverse("my_page")
        self.challenge_detail = reverse("challenge_detail", args=[1])
        self.knit_detail = reverse("knit_detail", args=[1])
        self.min_side_fullført_utfordring_url = reverse("complete")
        # Må legge til argumenter for å at urlen skal finnes
        self.min_side_avmeld_utfordring_url = reverse("delete", args=[1])
        self.min_side_avmeld_strikkekveld_url = reverse("delete_knit", args=[1])

        self.user1 = CustomUser.objects.create_user(username='test12', password='test12', name='AAron')
        self.user2 = CustomUser.objects.create_user(username='test123', password='test123', name='AAron1')
        self.knit1 = KnitNight.objects.create(
            knit_name="StarWars strikkekveld",
            description="Masse gøy starwars-strikking",
            time=datetime(2020, 4, 20, tzinfo=pytz.UTC),
            time_start=time(19, 30, 0),
            created_at=timezone.now(),
            created_by=self.user2
        )
        self.challenge1 = Challenge.objects.create(
            challenge_name="Hansker",
            description="Hansker med avtagbare fingre",
            rec_user_level="Legende",
            created_at=date(2020, 4, 12),
            created_by=self.user2
        )

        login = self.client.login(username='test123', password='test123')
        self.client.post(self.challenge_detail)
        self.client.post(self.knit_detail)

        self.assertTrue(login)

    def test_my_page_view(self):
        response = self.client.get(self.min_side_url)
        # Sjekker om den klarer å hente ned siden (HTTP-response code 200)
        self.assertEquals(response.status_code, 200)
        # Sjekker om den bruker riktig template
        self.assertTemplateUsed(response, "my_page.html")

    def test_knit_list(self):
        self.assertEquals(KnitNight.objects.all().count(), 1)

    # test til "complete challenge",
    """"
    def test_complete_challenge(self):
        response = self.client.post(self.min_side_fullført_utfordring_url)
        self.assertEquals(response.status_code,302)
        self.assertEquals(self.user2.completed_challenges, 1)
    """

    def test_deregister_challenge(self):
        # Antall påmeldte før avmelding
        self.assertEquals(Challenge.objects.all()[0].participants.count(), 1)
        # Avmelding
        response = self.client.post(self.min_side_avmeld_utfordring_url)
        self.assertEquals(response.status_code, 302)
        # Antall påmeldte etter avmelding
        self.assertEquals(Challenge.objects.all()[0].participants.count(), 0)

    def test_deregister_knitKnight(self):
        # Antall påmeldte før avmelding
        self.assertEquals(KnitNight.objects.all()[0].participants.count(), 1)
        # Avmelding
        response = self.client.post(self.min_side_avmeld_strikkekveld_url)
        self.assertEquals(response.status_code, 302)
        # Antall påmeldte etter avmelding
        self.assertEquals(KnitNight.objects.all()[0].participants.count(), 0)


class TestYarnUrl(TestCase):
    def setUp(self):
        self.annonse = reverse("yarn")
        self.lag_annonse = reverse("create_yarn")

    def test_url(self):
        self.assertEquals(resolve(self.annonse).func, yarnView)
        self.assertEquals(resolve(self.lag_annonse).func, create_yarn)


class TestYarnForm(TestCase):
    def test_valid_data(self):
        form = CreateYarn(data={
            "yarn_name": "blue yarn",
            "url": "cheapYarn.com",
            "description": "Very nice and thick wool yarn from one of the most awarded yarn company in the world."
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = CreateYarn(data={

        })
        self.assertFalse(form.is_valid())


class TestYarnViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.yarn_url = reverse("yarn")
        self.create_yarn_url = reverse("create_yarn")
        self.user1 = CustomUser.objects.create_user(username='test123', password='test123', name='AAron')
        self.user2 = CustomUser.objects.create_user(username='test1234', password='test1234', name='AAron1')
        self.yarn = Ads.objects.create(
            yarn_name="Garn",
            description="Feit garn",
            url="great-shit.com",
            created_at=date(2020, 4, 12),
            created_by=self.user2

        )
        login = self.client.login(username='test123', password='test123')

        self.assertTrue(login)

    def test_yarn_view(self):
        response = self.client.get(self.yarn_url)
        # Sjekker om den klarer å hente ned siden (HTTP-response code 200)
        self.assertEquals(response.status_code, 200)
        # Sjekker om den bruker riktig template
        self.assertTemplateUsed(response, "ads/yarn.html")



    def test_create_yarn(self):
        # Lager et objekt i databasen
        response = self.client.post(self.create_yarn_url, {

            "yarn_name": "yeboi",
            "url": "yeboi.com",
            "description": "Best thoing you'll ever get"
        }
                                    )
        # Sjekker at det er riktig http-response kode (302 fordi man blir redirectet til en annen url)
        self.assertEquals(response.status_code, 302)
        # Sjekker at det andre objektet har navnet "Heisann" (Første objektet er det som blir laget i setUp-metoden)
        self.assertEquals(Ads.objects.all()[1].yarn_name, "yeboi")

    def test_create_no_yarn(self):
        response = self.client.post(self.create_yarn_url)
        # Sjekker at det er riktig http-response kode (200 fordi man blir på samme side denne gangen)
        self.assertEquals(response.status_code, 200)
        # Sjekker at det andre objektet har navnet "Heisann" (Første objektet er det som blir laget i setUp-metoden)
        self.assertEquals(Ads.objects.all().count(), 1)

# Models-testing skjer implisitt i de andre test-metodene