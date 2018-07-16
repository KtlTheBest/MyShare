# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Song(models.Model):
    artist = models.CharField(max_length=20, default="Unknown")
    title = models.CharField(max_length=50, default="Unknown")
    song = models.FileField()

    user = models.ForeignKey(User, default=0)

    def __str__(self):
        return self.artist + ' - ' + self.title

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.song.storage, self.song.path

        # Delete the model before the file
        super(Song, self).delete(*args, **kwargs)

        # Delete the file after the model
        storage.delete(path)
