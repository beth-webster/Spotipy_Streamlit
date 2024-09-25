import musicbrainzngs as mbz
import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from mbz_helper_functions import (isrc_results_id)


# Set page configuration to wide for primary desktop use
st.set_page_config(layout="wide")

# Create dashboard sections
header = st.container()
identifier_input = st.container()
musicbrainz_output_info = st.container()
spotify_output_info = st.container()


# set User agent and hostname
mbz.set_useragent("bwebbo_music_data_app", "0.1", "bethawebster0@gmail.com")
mbz.set_hostname("beta.musicbrainz.org")



isrc_ready = 0
upc_ready = 0

with header:
    st.header('Data for digital tracks/bundles')

with identifier_input:
    col_isrc, col_or, col_upc = st.columns([3,1,3])
    with col_isrc:
        try:
            isrc_input = st.text_input("Enter ISRC:", "")
            
            if len(isrc_input) != 12:
                st.write('ISRC must be 12 characters')
                isrc_ready = 0
            else:
                isrc_ready = 1
        except:
            pass
    
    with col_or:
        col1, col2, col3 = st.columns(3)
        with col2:
            st.write('OR')  
    
    with col_upc:
        try:
            upc_input = st.text_input("Enter UPC:", "")
            
            if len(upc_input) != 12:
                st.write("UPC must be 13 digits... But this doesn't work yet")
                upc_ready = 0
            else:
                upc_ready = 1
        except:
            pass   
    
    if isrc_ready == 1:
        
        with musicbrainz_output_info:
            mbz_isrc_results = mbz.get_recordings_by_isrc(isrc_input)        
            mbz_track_id = isrc_results_id(mbz_isrc_results)        
            mbz_relase_results = mbz.get_recording_by_id(mbz_track_id, includes=['artist-credits', 'releases'])                      
            
            st.header('Music Brainz Info')
            st.write(mbz_isrc_results)
            st.write(mbz_relase_results)
            
        
        with spotify_output_info:
            st.header('Spotify Info')
            

            
            
            
            
            
            
            