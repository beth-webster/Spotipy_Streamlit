import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image
from helper_functions import id_from_url, get_artists, get_copyright, convert_df_csv, playlist_results, album_results, track_results


st.set_page_config(layout="wide")

header = st.container()
track_data = st.container()
bundle_data = st.container()


image = Image.open('Spotify_Logo_RGB_Green.png')
st.sidebar.image(image)


client_id = st.sidebar.text_input("Enter client ID:", "")
client_secret = st.sidebar.text_input("Enter client secret:", type="password")

if len(client_id) > 25 and len(client_secret) > 25 :
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = client_id,
                                                        client_secret = client_secret))


    with header:
        url = st.text_input("Enter URL:", "")
        url_type = id_from_url(url)[0]
        id = id_from_url(url)[1]

    if len(url) > 30:

        with track_data:
            st.write('Track Data')
            track_rows = []
            if url_type == 'album':
                results = album_results(sp, id)
                for track in results['tracks']['items']:
                    track_title = track.get('name')
                    track_number = track.get('track_number')
                    track_artist_names = get_artists(track) 
                    track_id = track.get('id')
                    results_tracks = track_results(sp, track_id)
                    isrc = results_tracks['external_ids'].get('isrc')
                    track_rows.append([isrc, track_title, track_artist_names, track_number])
                df = pd.DataFrame(track_rows, columns = ["ISRC", "Title", "Artist","Track Number"])

            elif url_type == 'playlist':
                results = sp.playlist(id, market = 'GB')
                for track in results['tracks']['items']:
                    if track['track'] is not None:
                        title = track['track'].get('name')
                        if track['track']['external_ids'] is not None:
                            isrc = track['track']['external_ids'].get('isrc')
                        else:
                            isrc = '-'                    
                        if track['track']['album'] is not None:
                            rel_date = track['track']['album'].get('release_date')
                        else:
                            rel_date = '-'
                        if track['track']['artists'] is not None:
                            artist_names = get_artists(track['track'])
                        else:
                            artist_names = []
                    else:
                        title = '-'
                    track_rows.append([isrc, title, artist_names, rel_date]) 
                df = pd.DataFrame(track_rows, columns = ["ISRC", "Title", "Artist", "Release date"])       
            
            elif url_type == 'track':
                results = track_results(sp,id)
                isrc = results['external_ids'].get('isrc')
                artist_names = get_artists(results)
                title = results.get('name')
                track_rows.append([isrc, title, artist_names])
                df = pd.DataFrame(track_rows, columns = ["ISRC", "Title", "Artist"])

            else:
                st.write('only Album, Playlist or Track links are currently supported')

            st.dataframe(df)
            csv = convert_df_csv(df)
            st.download_button(label = "Download track data as CSV"
                            , data = csv
                            , file_name = 'track_data.csv'
                            , mime = 'text/csv')


        with bundle_data:
            st.write('Bundle Data')
            bundle_rows = []
            if url_type == 'album':
                results = album_results(sp,id)
                bundle_upc = results['external_ids'].get('upc')
                label = results.get('label')
                bundle_rel_date = results.get('release_date')
                bundle_title = results.get('name')
                bundle_artists = get_artists(results) 
                bundle_copyright = get_copyright(results)
                bundle_rows.append([bundle_upc, bundle_title, bundle_artists, bundle_rel_date, label, bundle_copyright])
                df = pd.DataFrame(bundle_rows, columns = ["UPC", "Title", "Artist","Release Date", "Label", "Copyright"])

            elif url_type == 'playlist':
                results = playlist_results(sp, id)
                for track in results['tracks']['items']:
                    if track['track']is not None:
                        if track['track']['album'] is not None:
                            bundle_class = track['track']['album']['album_type']
                            bundle_id = track['track']['album']['id']
                            album_results_playlist = album_results(sp, bundle_id)
                            bundle_title = album_results_playlist.get('name')
                            bundle_artists = get_artists(album_results_playlist)
                            bundle_upc = album_results_playlist['external_ids'].get('upc')
                            bundle_label = album_results_playlist.get('label')
                            bundle_copyright = get_copyright(album_results_playlist)
                        else:
                            bundle_class = '-'
                            bundle_artists = '-'
                            bundle_title = '-'
                            bundle_upc = '-'
                            bundle_label = '-'
                    else:
                        bundle_class = '-'
                        bundle_artists = '-'
                        bundle_title = '-'
                        bundle_upc = '-'
                        bundle_label = '-'
                        bundle_copyright = '-'
                    bundle_rows.append([bundle_class, bundle_upc,  bundle_title, bundle_artists, bundle_label, bundle_copyright])
                df = pd.DataFrame(bundle_rows, columns = ["Class", "UPC", "Title", "Artist", "Label", "Copyright"])
            
            elif url_type == 'track':
                results = track_results(sp,id)
                bundle_id = results['album'].get('id')
                results_bundle = album_results(sp, bundle_id)
                bundle_upc = results_bundle['external_ids'].get('upc')
                label = results_bundle.get('label')
                bundle_rel_date = results_bundle.get('release_date')
                bundle_title = results_bundle.get('name')
                bundle_artists = get_artists(results_bundle)
                bundle_copyright = get_copyright(results_bundle) 
                bundle_rows.append([bundle_upc, bundle_title, bundle_artists, bundle_rel_date, label, bundle_copyright])
                df = pd.DataFrame(bundle_rows, columns = ["UPC", "Title", "Artist","Release Date", "Label", "Copyright"])

            else:
                st.write('only Album, Playlist or Track links are currently supported')

            st.dataframe(df)
            csv = convert_df_csv(df)
            st.download_button(label = "Download bundle data as CSV"
                            , data = csv
                            , file_name = 'bundle_data.csv'
                            , mime = 'text/csv')
    else:
        with track_data:
            st.write('Enter a spotify URL for an Album, Playlist or Track')
else:
   with header:
    st.write('Please enter login credentials')