from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_name', 'passport_no', 'date_of_birth', 'date', 'photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'client_name': forms.TextInput(attrs={'placeholder': 'Enter client name', 'class': 'form-input'}),
            'passport_no': forms.TextInput(attrs={'placeholder': 'Enter passport number', 'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-input-file', 'accept': 'image/*'}),
        }
