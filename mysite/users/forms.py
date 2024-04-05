from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible # widget=ReCaptchaV2Invisible

class UserRegisterForm(UserCreationForm):
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
    class Meta:
        model = Profile
        fields = ['profile_pic']