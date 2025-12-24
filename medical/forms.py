from django import forms
from .models import Client
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    is_staff = forms.BooleanField(label="Is Admin (Full Access)", required=False)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'is_active', 'is_staff']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    is_staff = forms.BooleanField(label="Is Admin (Full Access)", required=False)

    class Meta:
        model = User
        fields = ['username', 'is_active', 'is_staff']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_name', 'passport_no', 'date_of_birth', 'date', 'photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'client_name': forms.TextInput(attrs={'placeholder': 'Enter full name', 'class': 'form-input'}),
            'passport_no': forms.TextInput(attrs={'placeholder': 'Enter passport number', 'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-input-file', 'accept': 'image/*'}),
        }
