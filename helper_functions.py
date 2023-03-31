import re
import streamlit as st

def id_from_url(url):
    try:
        url_regex = re.search(r"^https?:\/\/(?:open\.)?spotify.com\/(user|episode|playlist|track|album)\/(?:spotify\/playlist\/)?(\w*)", url)

        return url_regex.group(1), url_regex.group(2)

    except AttributeError:
        return 'invalid URL'
    
@st.cache_data
def convert_df_csv(df):
    return df.to_csv(index = False,header=False)

def album_results(sp,id):
    return sp.album(id, market = 'GB')

def playlist_results(sp,id):
    return sp.playlist(id, market = 'GB')

def track_results(sp,id):
    return sp.track(id, market = 'GB')

@st.cache_data
def album_upc(album_info):
    upc = album_info['external_ids'].get('upc')
    return upc

@st.cache_data
def album_label(album_info):
    label = album_info.get('label')
    return label

@st.cache_data
def album_copyright(album_info):
    copyright_list = []
    for copyright in album_info['copyrights']:
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

@st.cache_data
def album_reldate(album_info):
    reldate = album_info.get('release_date')
    return reldate

@st.cache_data
def album_title(album_info):
    title = album_info.get('name')
    return title

@st.cache_data
def album_numtracks(album_info):
    numtracks = album_info.get('total_tracks')
    return int(numtracks)

@st.cache_data
def album_trackid(track):
    trackid = track.get('id')
    return trackid

@st.cache_data
def album_trackseq(track):
    trackseq = track.get('track_number')
    return trackseq

@st.cache_data
def track_isrc(track_info):
    isrc = track_info['external_ids'].get('isrc')
    return isrc

@st.cache_data
def artists(track):
    artist_list = []
    for artist in track['artists']:
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

@st.cache_data
def track_title(track):
    title = track.get('name')
    return title

@st.cache_data
def playlist_bundleid(track):
    bundleid = track['track']['album']['id']
    return bundleid

@st.cache_data
def track_bundleid(track_info):
    bundleid = track_info['album'].get('id')
    return bundleid

def create_code_txt(barcodes):
    flat_barcodes = [item for sublist in barcodes for item in sublist]
    padded_barcodes = []
    for num in flat_barcodes:
        str_num = str(num)
        str_num = str_num.zfill(13)
        if len(str_num) > 13:
            # If the number is longer than 13 digits, trim any leading zeros
            str_num = str_num.lstrip('0')
            str_num = str_num.zfill(13)
        padded_barcodes.append(str_num)
    delimited_barcodes = ',\n'.join([f"'{num}'" for num in padded_barcodes])
    held_bundle_search = (f"select *\nfrom held_candidate_bundles\nwhere barcode in ({delimited_barcodes})")
    return held_bundle_search