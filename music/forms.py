from django import forms
from django.contrib.auth.models import User
from .models import Song
from django.db.models import Q
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
    username = forms.CharField(max_length=30, min_length=3)
    password = forms.CharField(max_length=40, min_length=8, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


class UploadForm(forms.ModelForm):
    title = forms.CharField(max_length=30, min_length=1)
    artist = forms.CharField(max_length=30, min_length=1)
    song = forms.FileField()

    def is_valid(self):
        valid = super(UploadForm, self).is_valid()
        if not valid:
            return False

        data_type, sub = self.cleaned_data['song'].content_type.split('/')
        if data_type != 'audio' or sub != 'mp3':
            return False
        
        return True

    class Meta:
        model = Song
        exclude = ('user',)
