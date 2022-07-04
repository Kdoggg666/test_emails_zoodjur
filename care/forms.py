from django import forms
from .models import Care


class CareForm(forms.ModelForm):

    class Meta:
        model = Care
        fields = '__all__'
        labels = {
                'name': 'Djurens namn',
                'care_guide': 'Allmän vård',
                'cage_setup': 'Krav på bur',
                'lighting': 'Belysningskrav',
                'heating': 'Värmekrav',
                'feeding_schedule': 'Utfodringskrav',
                'known_problems': 'Möjliga hälsoproblem',
                'other_information': 'Ytterligare läsning URL',
                'other_information_name': 'Ytterligare läsning Namn',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
