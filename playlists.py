import os
import random
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import spotipy

def word_to_two(w):
    return " ".join(w.split(" ")[0:2])

def get_playlist(clientID, clientSECRET, keyword):
    client_credentials_manager = SpotifyClientCredentials(clientID,clientSECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    """
    Input an emotion and the Spotify API will output a random public playlist accordingly
    """
    emotions = {'neutral' : ['neutral', 'popular', 'hits', 'dance', 'hot', 'top'],
                'joy' : ['happiness', 'happy', 'cheerful', 'summer', 'upbeat', 'party'],
                'anger' : ['angry', 'anger', 'rage', 'upset'],
                'sorrow' : ['sad', 'sadness', 'emo', 'winter'],
                'surprise' : ['shock', 'surprise'],
                'fear' : ['calm', 'calming', 'relax']}

    if keyword in emotions.keys():
        keyword = random.choice(emotions[keyword])

    random_int = random.randint(0, 75)
    keyword_search = word_to_two(keyword)
    playlist_list = sp.search(keyword_search, limit=10, offset=random_int, type='playlist', market='US')['playlists']['items']

    for pl in playlist_list:
        if pl['public'] is None or pl['public'] == True:
            return pl['external_urls']['spotify']
