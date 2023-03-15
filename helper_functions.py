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
    
def id_from_url_for_file(url):
    try:
        url_regex = re.search(r"\['([^']+)'\]", url)

        return url_regex.group(1)

    except AttributeError:
        return 'invalid URL'

def get_artists(results):
    artist_list = []
    for artist in results['artists']:
        try:
            for key in artist:
                try:
                    if key == 'name':
                        artist_list.append((artist[key]))
                except:
                    pass
        except:
            pass
    artists = '/'.join([str(artist) for artist in artist_list])
    return artists

def get_copyright(results):
    copyright_list = []
    for copyright in results['copyrights']:
        try:
            for key in copyright:
                try:
                    if key == 'text':
                        copyright_list.append((copyright[key]))
                except:
                    pass
        except:
            pass
    copyrights = '/'.join([str(copyright) for copyright in copyright_list])
    return copyrights

def ablumtracks_title_artist_num_id(track):
    track_title = track.get('name')
    track_number = track.get('track_number')
    track_artist_names = get_artists(track) 
    track_id = track.get('id')
    return track_title, track_artist_names, track_number, track_id

def tracks_isrc_artirst_title(track_info):
    isrc = track_info['external_ids'].get('isrc')
    artist_names = get_artists(track_info)
    title = track_info.get('name')
    return isrc, artist_names, title
    
def playlisttracks_isrc_title_artitst_date(track):
    try:
        title = track['track'].get('name')
        try:
            isrc = track['track']['external_ids'].get('isrc')
            rel_date = track['track']['album'].get('release_date')
            artist_names = get_artists(track['track'])
        except:
            artist_names = []
    except:
        pass
    return isrc, title, artist_names, rel_date

def album_upc_lab_date_title_artitst_copy(album_info):
    bundle_upc = album_info['external_ids'].get('upc')
    label = album_info.get('label')
    bundle_rel_date = album_info.get('release_date')
    bundle_title = album_info.get('name')
    bundle_artists = get_artists(album_info) 
    bundle_copyright = get_copyright(album_info)
    bundle_url = album_info['external_urls'].get('spotify')
    num_tracks = album_info.get('total_tracks')
    if int(num_tracks)>4:
        price = 425
        bundle_class = "A"
    else:
        price = 40
        bundle_class = "S"
    return bundle_upc, label, bundle_rel_date, bundle_title, bundle_artists, bundle_copyright, num_tracks, price, bundle_class, bundle_url

def playlist_class_num_art_title_upc_lab_copy_url(track, sp):
    try:
        bundle_class = track['track']['album']['album_type']
        bundle_id = track['track']['album']['id']
        album_results_playlist = album_results(sp, bundle_id)
        bundle_title = album_results_playlist.get('name')
        bundle_artists = get_artists(album_results_playlist)
        bundle_upc = album_results_playlist['external_ids'].get('upc')
        num_tracks = album_results_playlist.get('total_tracks')
        bundle_label = album_results_playlist.get('label')
        bundle_copyright = get_copyright(album_results_playlist)
        bundle_url = album_results_playlist['external_urls'].get('spotify')
    except:
        pass
    return bundle_class, num_tracks, bundle_artists, bundle_title, bundle_upc, bundle_label, bundle_copyright, bundle_url


@st.cache
def convert_df_csv(df):
    return df.to_csv(index = False,header=False)

@st.cache
def album_results(sp,id):
    return sp.album(id, market = 'GB')

@st.cache
def playlist_results(sp,id):
    return sp.playlist(id, market = 'GB')

@st.cache
def track_results(sp,id):
    return sp.track(id, market = 'GB')