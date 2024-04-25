from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible # widget=ReCaptchaV2Invisible

class UserRegisterForm(UserCreationForm):
    """
        Formularz rejestracji użytkownika.

        Pola:
            username (CharField): Pole do wprowadzenia nazwy użytkownika.
            email (EmailField): Pole do wprowadzenia adresu e-mail.
            first_name (CharField): Pole do wprowadzenia imienia użytkownika.
            last_name (CharField): Pole do wprowadzenia nazwiska użytkownika.
            password1 (CharField): Pole do wprowadzenia hasła.
            password2 (CharField): Pole do potwierdzenia hasła.
            captcha (ReCaptchaField): Pole do potwierdzenia, że użytkownik nie jest robotem.

    """

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    captcha = ReCaptchaField()
    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'password1', 'password2', 'captcha']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
        }

class UserUpdateForm(forms.ModelForm):
    """
        Formularz aktualizacji danych użytkownika.

        Pola:
            username (CharField): Pole do wprowadzenia nazwy użytkownika.
            first_name (CharField): Pole do wprowadzenia imienia użytkownika.
            last_name (CharField): Pole do wprowadzenia nazwiska użytkownika.
            email (EmailField): Pole do wprowadzenia adresu e-mail.

    """

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form_control', 'placeholder': 'Wprowadź email'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Wprowadź nick'}),
            'first_name': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Wprowadź imie'}),
            'last_name': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Wprowadź nazwisko'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    """
       Formularz aktualizacji danych profilowych użytkownika.

       Pola:
           profile_pic (ImageField): Pole do wyboru nowego zdjęcia profilowego.

    """

    class Meta:
        model = Profile
        fields = ['profile_pic']