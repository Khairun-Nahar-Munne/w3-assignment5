from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class PropertyOwnerSignupForm(forms.ModelForm):
    username = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Username', 
            'autocomplete': 'off'
        })
    )
    email = forms.EmailField(
        max_length=50, 
        required=True, 
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email', 
            'autocomplete': 'off'
        })
    )
    first_name = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name', 
            'autocomplete': 'off'
        })
    )
    last_name = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name', 
            'autocomplete': 'off'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password', 
            'autocomplete': 'new-password'
        }),
        min_length=8
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user