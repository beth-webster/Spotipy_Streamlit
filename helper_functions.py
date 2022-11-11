import re
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def id_from_url(url):
    try:
        url_regex = re.search(r"^https?:\/\/(?:open\.)?spotify.com\/(user|episode|playlist|track|album)\/(?:spotify\/playlist\/)?(\w*)", url)

        return url_regex.group(1), url_regex.group(2)

    except AttributeError:
        return 'invalid URL'

def get_artists(results):
    artist_list = []
    for artist in results['artists']:
        for key in artist:
                if key == 'name':
                    artist_list.append((artist[key]))
    artists = '/'.join([str(artist) for artist in artist_list])
    return artists

@st.cache
def convert_df_csv(df):
    return df.to_csv()

@st.cache
def album_results(sp,id):
    return sp.album(id, market = 'GB')

@st.cache
def playlist_results(sp,id):
    return sp.playlist(id, market = 'GB')

@st.cache
def track_results(sp,id):
    return sp.track(id, market = 'GB')

