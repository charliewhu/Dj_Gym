from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from accounts.models import User
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    email = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control mb-2',
                                   'placeholder': 'User name'}))
    password1 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control mb-2',
                                   'placeholder': 'Password'}))

    password2 = forms.CharField(label=_("Please Re-Enter Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control mb-2',
                                   'placeholder': 'Re-Enter Password'}))                               


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Password'}))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)
