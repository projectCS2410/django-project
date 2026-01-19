from django import forms

from .models import FilmComment


class FilmCommentForm(forms.ModelForm):
    class Meta:
        model = FilmComment
        fields = ['film_title', 'text']
        widgets = {
            'film_title': forms.HiddenInput(),
            'text': forms.Textarea(
                attrs={
                    'rows': 2,
                    'placeholder': 'Write a comment…',
                }
            ),
        }
