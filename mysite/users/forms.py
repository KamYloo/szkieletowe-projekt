from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible # widget=ReCaptchaV2Invisible

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    captcha = ReCaptchaField()
    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'password1', 'password2', 'captcha'] #


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']