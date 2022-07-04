from django import forms
from .models import Animal, Rating


class AnimalForm(forms.ModelForm):

    class Meta:
        model = Animal
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ['title', 'content', 'rating_out_of_five', 'animal']
        labels = {
            'title': 'Review Name',
            'content': 'Write your review here',
            'animal': 'Animal Name',
            'rating_out_of_five': 'Rate this animal from 1 to 5'
        }
        hidden = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
