import streamlit as st

def isrc_results_id(isrc_results):
    recording_list = isrc_results['isrc']['recording-list']
    if len(recording_list) > 0:
        track_id = recording_list[0].get('id', None)
    return track_id