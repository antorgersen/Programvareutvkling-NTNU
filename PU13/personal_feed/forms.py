from django import forms
from . import models
from .models import Personal_Feed_Post


class Create_Personal_Feed_Post_Form(forms.ModelForm):
    title = forms.CharField(label="Tittel",
                            widget=forms.TextInput(attrs={'placeholder': 'Tittel'}),
                            )
    content = forms.CharField(label="Innhold",
                              widget=forms.Textarea(attrs={'placeholder': 'Dette innlegget er om ..'}),
                            )

    class Meta:
        model = Personal_Feed_Post
        fields = ['title', 'content']