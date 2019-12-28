from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages
from .forms import SongForm
from .calls import get_auth_token, search_song, queue_song, skip_song, get_current_track_uri, get_playlist_tracks, find_pos
from .models import Song


def search_home(request):
    if request.method == 'POST':
        # make auth request here
        form = SongForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            #Couple things to do: validate song, log song in a database if valid, 
            # make API call on valid song, reroute to 'picksong/' with all search results
            
            auth_token = get_auth_token()
            searched_song_id = search_song(auth_token, form.cleaned_data['your_song']) #For now I am just receiving one ID corresponding to the first result from search rather than top X results

            #Insert the result(song+searched_song_id) into a Database for queueing purposes/future data analytics
            song_instance = Song()
            song_instance.searched_song = form.cleaned_data['your_song']
            song_instance.song_id = searched_song_id
            song_instance.save()

            # We will queue up the single song here as well FOR NOW, need to research if this is robust against multiple people queueing at the same time
            _ = queue_song(auth_token, searched_song_id)


            # 1. After queing, we want to give the user a confirmation of their queue
            # 2. We also want to give them their position in queue. Can implement by checking absolute position
            #  in playlist and subtracting position of current song to get a relative position aka a pseudo-queue
            #  in the playlist(   bc spotify doesnt have a queue endpoint :(    )
            queued_song_relative_pos = find_pos(auth_token) # Display this position to the user 

            # Now we send some sort of popup message to the user saying that track has been queued at position: queued_song_relative_pos
            msg = 'Your song has been queued at position: ' + str(queued_song_relative_pos)
            messages.info(request, msg)

            # Add functionality to SKIP song directly on the home page!!! aka in THIS view
            #  i.e add buttion to allow user to vote and display a bar showing the votes so far.
            #  When votes reach threshold call skip function



            return HttpResponseRedirect('/') # redirect to same page aka reload so that they can queue again!
    else:
        form = SongForm()
    return render(request, 'search/search_home.html', {'form': form})

    # return render(request,'search/search_home.html')

def confirmation(request):
    # Implement
    return render(request,'search/confirmation_home.html')


#def skip_song(request):
    #Implement
#    return render(request, 'search/skip_home.html')





# 'picksong/: user will click on button to pick the appropriate song or go back, make API call to queue up this song and 
# reroute to 'confirmation/'. 

# 'confirmation/' allow user to skip current song or reroute back to '/'. Also displays current position of their song in queue

# ^^^ JK, we can just display an alert box saying "YOUR SONG HAS BEEN QUEUED AT POSITION X"

# you can get to the /skip/ page from the home page when you hit skip button. 