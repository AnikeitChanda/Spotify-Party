from django.db import models
from django.utils import timezone

# Create your models here.
class Song(models.Model):
    searched_song = models.CharField(max_length=100)
    song_id = models.TextField()
    date_searched = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.searched_song