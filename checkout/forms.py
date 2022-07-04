from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)
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
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Fullständiga namn',
            'email': 'E-post Adress',
            'phone_number': 'Telefonnummer',
            'postcode': 'postnummer',
            'town_or_city': 'Stad',
            'street_address1': 'Gatuadresss 1',
            'street_address2': 'Gatuadress 2',
            'county': 'Län',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
