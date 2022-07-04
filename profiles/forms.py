from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        labels = {
            'default_phone_number': 'Telefonnummer',
            'default_postcode': 'Postnummer',
            'default_town_or_city': 'Stad',
            'default_street_address1': 'Gatuadress 1',
            'default_street_address2': 'Gatuadress 2',
            'default_county': 'Län',
            'default_country': 'Land',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
