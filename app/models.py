from django.db import models
from django.contrib.auth.models import User

class Album(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spotify_id = models.CharField(max_length=200)
    # Add other fields like release date, image URL, etc.
    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Add other fields like genres, popularity, etc.
    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.user.username