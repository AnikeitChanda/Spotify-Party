import requests
import json
from .secrets import *

def get_auth_token():
    #move to a secure file later
    refresh_token = sec_refresh_token
    params = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
    url = 'https://accounts.spotify.com/api/token'
    #move to a secure file later
    x = requests.post(url, data = params, headers = { 'Authorization': sec_auth_code})
    return x.json()['access_token']


def search_song(auth_token, song):
    url = 'https://api.spotify.com/v1/search'
    pay = {'q': song, 'type': 'track'}
    header_str = {'Authorization': 'Bearer ' + auth_token}
    x = requests.get(url, params = pay, headers = header_str)
    return x.json()['tracks']['items'][0]['uri'] # Id of Top searchhit - might need to give more hits and allow user to search


def get_playlists(auth_token):
  url = 'https://api.spotify.com/v1/me/playlists'
  pay = {'limit': 50}
  header_str = {'Authorization': 'Bearer ' + auth_token}
  x = requests.get(url, params = pay, headers = header_str)
  return x


def queue_song(auth_token, uri):
  playlist_id = sec_playlist_id #move to a secure file later
  url = 'https://api.spotify.com/v1/playlists/'+playlist_id+'/tracks'
  pay = {'uris': [uri]}
  header_str = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + auth_token}
  x = requests.post(url, data = json.dumps(pay), headers = header_str)
  return x.json()['snapshot_id']


def skip_song(auth_token):
    url = 'https://api.spotify.com/v1/me/player/next'
    header_str = {'Authorization': 'Bearer ' + auth_token}
    x = requests.post(url, headers = header_str)
    return x


def get_current_track_uri(auth_token):
  url = 'https://api.spotify.com/v1/me/player/currently-playing'
  header_str = {'Authorization': 'Bearer ' + auth_token}
  pay = {'market': 'US'}
  x = requests.get(url, params = pay, headers = header_str)
  return x.json()['item']['uri']


def get_playlist_tracks(auth_token):
  playlist_id = sec_playlist_id #move to a secure file later
  url = 'https://api.spotify.com/v1/playlists/'+playlist_id+'/tracks'
  header_str = {'Authorization': 'Bearer ' + auth_token}
  pay = {'market': 'US', 'fields':'total, items(track(uri))', 'limit': 100, 'offset':0}
  x = requests.get(url, params = pay, headers = header_str)
  x = x.json()
  return x['items'], x['total']


def find_pos(auth_token):
  curr_track_uri = get_current_track_uri(auth_token)
  playlist_items, total_items = get_playlist_tracks(auth_token)
  curr_track_position = 0 # dummy value
  for count, dic in enumerate(playlist_items):
    if curr_track_uri == dic['track']['uri']:
      curr_track_position = count + 1
      break
  queued_song_relative_pos = total_items - curr_track_position
  return queued_song_relative_pos



# also much later need to add API+GUI way to shuffle around songs that have been added. Can only expose this function to admin
    