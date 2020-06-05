from django import forms


# Form for creating a challenge
class CreateChallenge(forms.Form):
    challenge_name = forms.CharField(label="Utfordring", max_length="200")

    choice = (('Nybegynner', 'Nybegynner'), ('Amatør', 'Amatør'), ('Erfaren', 'Erfaren'), ('Proff', 'Proff'),
              ('Legende', 'Legende'),)
    rec_user_level = forms.ChoiceField(choices=choice, label='Anbefalt brukernivå')

    description = forms.CharField(widget=forms.Textarea, label="Beskrivelse", max_length="500")


class CreateKnit(forms.Form):
    knit_name = forms.CharField(label="Strikkekveld", max_length="200")
    time = forms.DateTimeField(label="Tidspunkt (yyyy-mm-dd)")
    time_start = forms.TimeField(label="Tidspunkt (yyyy-mm-dd)")
    description = forms.CharField(widget=forms.Textarea, label="Beskrivelse", max_length="500")


class CreateYarn(forms.Form):
    yarn_name = forms.CharField(label="Garn", max_length="200")
    url = forms.CharField(label="Nettsted", max_length="200")
    description = forms.CharField(widget=forms.Textarea, label="Beskrivelse", max_length="500")
