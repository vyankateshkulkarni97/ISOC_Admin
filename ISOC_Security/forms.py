from django import forms
from django.contrib.auth.forms import  AuthenticationForm
from ISOC_Security.models import ISOC_User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate



class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password1 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if ISOC_User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if ISOC_User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password1 = cleaned_data.get("password1")

        if password and password1 and password != password1:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
    



class CustomUserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        print('Cleaning data: Username:', username)
        print('Cleaning data: Password:', password)

        if username and password:
            user = authenticate(username=username, password=password)
            print('Authenticated user:', user)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")
            elif not user.is_active:
                raise forms.ValidationError("This account is inactive.")
            self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)