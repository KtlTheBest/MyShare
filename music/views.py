# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import generic
from django.views.generic.edit import CreateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm, UploadForm
from .models import Song
from django.http import HttpResponseRedirect
from django import forms

# Create your views here


class IndexPage(generic.ListView):
    template_name = 'music/index.html'
    model = Song
    context_object_name = 'all_songs'

    def get_queryset(self):
        return Song.objects.all()


class AddSong(generic.View):

    template_name = 'music/add_song.html'

    def get(self, request):
        upload_form = UploadForm()
        return render(request, self.template_name, {
            'form': upload_form
        })

    def post(self, request):
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            song = upload_form.save()
            song.user = request.user
            song.save()
            return redirect('music:add_song')
        else:
            return render(request, self.template_name,{
                'form': upload_form,
            })


class SongDetail(generic.DetailView):
    model = Song
    template_name = 'music/song_detail.html'
    context_object_name = 'song_entry'


class DeleteSong(DeleteView):
    model = Song
    success_url = reverse_lazy('music:profile')


class SignUpView(generic.View):
    form = SignUpForm
    user = User
    template_name = 'music/signup.html'

    def get(self, request):
        return render(request, self.template_name, {
            'form': self.form(),
        })

    def post(self, request):
        form = SignUpForm(request.POST)

        user = User()

        if form.is_valid():
            user = form.save()
            #if request.POST['password'] != request.POST['password_retry']:
            #    return render(request, self.template_name, {
            #        'form': form,
            #        'error_message': 'Password mismatch!'
            #    })

            user.set_password(request.POST['password'])
            user.save()

            auth_user = authenticate(username=user.username, password=request.POST['password'])
            login(request, auth_user)

            return redirect('music:index')
        else:
            return render(request, self.template_name, {
                'form': form,
            })


class LoginView(generic.View):
    form = LoginForm
    template_name = 'music/login.html'

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('music:index')
            else:
                print("User is disabled")
        else:
            return render(request, 'music/login.html', {'error': "Wrong Username/Password!", 'form': self.form})


class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        return redirect('music:index')


class DetailsView(generic.DetailView):
    model = Song
    context_object_name = 'song'
    template_name = 'music/details.html'


class ProfileView(generic.ListView):
    context_object_name = 'songs'
    template_name = 'music/profile.html'

    def get_queryset(self):
        return Song.objects.filter(user=self.request.user)
