from django import forms

class SongForm(forms.Form):
    your_song = forms.CharField(label='your song', max_length=100)