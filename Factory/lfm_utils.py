import json
import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv
token = getenv("LASTFM_TOKEN")
api_url = "http://ws.audioscrobbler.com/2.0/"
user_agent = "Essence/1.0.0 ( https://github.com/EssenceHub )"

def album_search(album_name: str, album_artist: str):
    headers = {'user-agent': user_agent}
    params = {"api_key": token, "method": "album.getInfo", "album": album_name, "artist": album_artist, "format": "json"}
    r = requests.post(api_url, headers=headers, data=params)
    return r.json()['album']

def artist_search(artist_name: str):
    headers = {'user-agent': user_agent}
    params = {"api_key": token, "method": "artist.getInfo", "artist": artist_name, "format": "json"}
    r = requests.post(api_url, headers=headers, data=params)
    return r.json()['artist']

def get_artist_top_songs(artist_name: str):
     headers = {'user-agent': user_agent}
     params = {"api_key": token, "method": "artist.getTopTracks", "artist": artist_name, "limit": '1', "format": "json"}
     r = requests.post(api_url, headers=headers, data=params)
     return r.json()['toptracks']['track']
 
 
def get_artist_top_albums(artist_name: str):
     headers = {'user-agent': user_agent}
     params = {"api_key": token, "method": "artist.getTopAlbums", "artist": artist_name, "limit": '1', "format": "json"}
     r = requests.post(api_url, headers=headers, data=params)
     return r.json()['topalbums']['album']
 

def get_album_tracks(album_name: str, artist_name: str):
    album = album_search(album_name, artist_name)
    amount_of_tracks = len(album['tracks']['track'])
    tracks = ""
    
    for track in range(0, amount_of_tracks):
        tracks += (f"{track+1}: {album['tracks']['track'][track]['name']}\n")
    
    return tracks


def get_album_tags(album_name: str, artist_name: str):
    album = album_search(album_name, artist_name)
    amount_of_tags = len(album['tags']['tag'])
    tags = ""
    
    for tag in range(0, amount_of_tags):
        tags += (f"{album['tags']['tag'][tag]['name']}\n")
    
    return tags
    

# def get_artist_image(mbid: str):
#     headers = {'user-agent': user_agent, "accept": "application/json"}
#     url = f'https://musicbrainz.org/ws/2/artist/{mbid}?inc=url-rels'
#     r = requests.get(url, headers=headers)
#     print(json.dumps(r.text, sort_keys=True, indent=4))
#     print(r.text)