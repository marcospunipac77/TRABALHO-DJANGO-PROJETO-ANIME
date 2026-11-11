from django import forms

from .models import Anime


class AnimeForm(forms.ModelForm):
    class Meta:
        model = Anime
        fields = ["title", "synopsis", "release_year", "status", "poster_url", "genres"]
        widgets = {
            "synopsis": forms.Textarea(attrs={"rows": 5}),
            "genres": forms.CheckboxSelectMultiple(),
        }
