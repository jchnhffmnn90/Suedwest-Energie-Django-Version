from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        label='Name / Firma',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control py-3',
            'placeholder': 'Ihre Firma GmbH',
            'id': 'name'
        })
    )
    contact_person = forms.CharField(
        label='Ansprechpartner',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control py-3',
            'placeholder': 'Max Mustermann',
            'id': 'contact_person'
        })
    )
    email = forms.EmailField(
        label='E-Mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-control py-3',
            'placeholder': 'name@firma.de',
            'id': 'email'
        })
    )
    phone = forms.CharField(
        label='Telefon',
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control py-3',
            'placeholder': '+49 ...',
            'id': 'phone'
        })
    )
    message = forms.CharField(
        label='Nachricht',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Wie können wir Ihnen helfen?',
            'id': 'message'
        })
    )
