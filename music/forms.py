from django import forms
from django.contrib.auth.models import User
from .models import Song
from django.contrib.auth.forms import UserCreationForm


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=30, min_length=3)
    password = forms.CharField(max_length=40, min_length=8, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', )


class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=30, min_length=3)
    password = forms.CharField(max_length=40, min_length=8, widget=forms.PasswordInput)
    password_retry = forms.CharField(max_length=40, min_length=8, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_retry')


class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=30, min_length=3)
    password = forms.CharField(max_length=40, min_length=8, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


class UploadForm(forms.ModelForm):
    title = forms.CharField(max_length=30, min_length=1)
    artist = forms.CharField(max_length=30, min_length=1)
    song = forms.FileField()
    user = forms.MultipleChoiceField(widget=forms.HiddenInput)

    class Meta:
        model = Song
        fields = ('title', 'artist', 'song', 'user')
