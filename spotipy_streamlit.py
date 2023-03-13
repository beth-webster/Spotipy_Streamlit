import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image
from helper_functions import id_from_url, id_from_url_for_file, ablumtracks_title_artist_num_id, tracks_isrc_artirst_title, playlisttracks_isrc_title_artitst_date, album_upc_lab_date_title_artitst_copy, playlist_class_num_art_title_upc_lab_copy_url, convert_df_csv, playlist_results, album_results, track_results


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
                album_info = album_results(sp, id)
                for track in album_info['tracks']['items']:
                    try:
                        track_title, track_artist_names, track_number, track_id = ablumtracks_title_artist_num_id(track)
                        track_info = track_results(sp, track_id)
                    except:
                        pass
                    for track_id in track_info:
                        try:
                            isrc = tracks_isrc_artirst_title(track_info)[0]
                        except:
                            pass
                    track_rows.append([isrc, track_title, track_artist_names, track_number])
                df = pd.DataFrame(track_rows, columns = ["ISRC", "Title", "Artist","Track Number"])

            elif url_type == 'playlist':
                results = sp.playlist(id, market = 'GB')
                for track in results['tracks']['items']:
                    try:
                        isrc, title, artist_names, rel_date = playlisttracks_isrc_title_artitst_date(track)
                    except:
                        pass
                    track_rows.append([isrc, title, artist_names, rel_date]) 
                df = pd.DataFrame(track_rows, columns = ["ISRC", "Title", "Artist", "Release date"])       
            
            elif url_type == 'track':
                track_info = track_results(sp,id)
                isrc, artist_names, title = tracks_isrc_artirst_title(track_info)
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
                album_info = album_results(sp,id)
                bundle_upc, label, bundle_rel_date, bundle_title, bundle_artists, bundle_copyright, num_tracks, price, bundle_class = album_upc_lab_date_title_artitst_copy(album_info)
                bundle_rows.append([bundle_upc, bundle_title, bundle_artists, bundle_rel_date, label, bundle_copyright])
                df = pd.DataFrame(bundle_rows, columns = ["UPC", "Title", "Artist","Release Date", "Label", "Copyright"])

            elif url_type == 'playlist':
                urls_rows_for_files = []
                playlist_info = playlist_results(sp, id)
                for track in playlist_info['tracks']['items']:
                    try:
                        bundle_class, num_tracks, bundle_artists, bundle_title, bundle_upc, bundle_label, bundle_copyright, bundle_url = playlist_class_num_art_title_upc_lab_copy_url(track, sp)
                        bundle_rows.append([bundle_class, num_tracks, bundle_upc,  bundle_title, bundle_artists, bundle_label, bundle_copyright, bundle_url])
                        urls_rows_for_files.append([bundle_url])
                    except:
                        pass
                df = pd.DataFrame(bundle_rows, columns = ["Class", "Number_of_Tracks","UPC", "Title", "Artist", "Label", "Copyright", "Bundle_URL"])
                track_file_rows = []
                tracklisting_file_rows = []
                bundle_file_rows = []
                for file_url in urls_rows_for_files:
                    try:
                        ext_str_file_url = id_from_url_for_file(str(file_url))
                        file_url_type, file_url_id = id_from_url(ext_str_file_url)
                        if file_url_type == 'album':
                            files_album_info = album_results(sp,file_url_id)
                            bundle_upc, label, bundle_rel_date, bundle_title, bundle_artists, bundle_copyright, num_tracks, price, bundle_class = album_upc_lab_date_title_artitst_copy(files_album_info)
                        elif url_type == 'track':
                            track_info = track_results(sp,id)
                            bundle_id = track_info['album'].get('id')
                            files_album_info = album_results(sp, bundle_id)
                            bundle_upc, label, bundle_rel_date, bundle_title, bundle_artists, bundle_copyright, num_tracks, price, bundle_class = album_upc_lab_date_title_artitst_copy(album_info)
                        bundle_file_rows.append([bundle_upc,"",bundle_title,bundle_artists,"",bundle_class,"A",label,label,label,bundle_copyright,price,"","",num_tracks])

                    except:
                        pass
                bundle_file_df = pd.DataFrame(bundle_file_rows)
                
            elif url_type == 'track':
                track_info = track_results(sp,id)
                bundle_id = track_info['album'].get('id')
                album_info = album_results(sp, bundle_id)
                bundle_upc, label, bundle_rel_date, bundle_title, bundle_artists, bundle_copyright, num_tracks, price, bundle_class = album_upc_lab_date_title_artitst_copy(album_info)
                bundle_rows.append([bundle_upc, bundle_title, bundle_artists, bundle_rel_date, label, bundle_copyright])
                df = pd.DataFrame(bundle_rows, columns = ["UPC", "Title", "Artist","Release Date", "Label", "Copyright"])

            else:
                st.write('only Album, Playlist or Track links are currently supported')

            st.dataframe(df)
            csv = convert_df_csv(df)
            st.download_button(label = "Download above table as CSV"
                            , data = csv
                            , file_name = 'bundle_data.csv'
                            , mime = 'text/csv')
            
            bundle_csv = convert_df_csv(bundle_file_df)
            st.download_button(label = "Download bundle data as CSV to load"
                            , data = bundle_csv
                            , file_name = 'bundle_data.csv'
                            , mime = 'text/csv')
            
    else:
        with track_data:
            st.write('Enter a spotify URL for an Album, Playlist or Track')
else:
   with header:
    st.write('Please enter login credentials')