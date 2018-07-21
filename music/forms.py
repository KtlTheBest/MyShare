from django import forms
from django.contrib.auth.models import User
from .models import Song
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=30, min_length=3, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Your Username',
        }
    ))
    password = forms.CharField(max_length=40, min_length=8, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Your Password',
        }
    ))
    password_retry = forms.CharField(max_length=40, min_length=8, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password Again',
        }
    ))

    def is_valid(self):
        valid = super(SignUpForm, self).is_valid()

        if not valid:
            return False

        if User.objects.filter(username=self.cleaned_data['username']):
            return False

        if self.cleaned_data['password'] != self.cleaned_data['password_retry']:
            return False

        return True

    class Meta:
        model = User
        fields = ('username', 'password', 'password_retry')


class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=30, min_length=3, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Your Username',
            #'id': 'id_Username',
        }
    ))
    password = forms.CharField(max_length=40, min_length=8, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Your Password',
            #'id': 'id_Password',
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'password')


class UploadForm(forms.ModelForm):
    title = forms.CharField(max_length=30, min_length=1, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Title',
        }
    ))
    artist = forms.CharField(max_length=30, min_length=1, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Artist',
        }
    ))
    song = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'custom-file-input',
        }
    ))

    def is_valid(self):
        valid = super(UploadForm, self).is_valid()
        if not valid:
            return False

        data_type, sub = self.cleaned_data['song'].content_type.split('/')
        if data_type != 'audio' or sub not in ('mp3', 'flac'):
            return False

        return True

    class Meta:
        model = Song
        exclude = ('user',)
