import streamlit as st
import re

# Functions
def ids_from_urls(at_links):
    id_list = []
    for url in at_links:
        try:
            url_regex = re.search(r"(?<=i=)\d+", url)
            
            if url_regex:
                id_list.append(url_regex.group())

        except AttributeError:
            id_list.append('invalid input')
    
    return id_list

# Set page configuration to wide for primary desktop use
st.set_page_config(layout="wide")

# Create dashboard sections
header = st.container()
links_input = st.container()
output_ids = st.container()

# Header Sction of page
with header:
    st.write("Extract IDs from iTunes links, add into code")
    
# Main page section
with links_input:
    links_ready = 0
    
    at_links = st.text_area('Paste links here')
    at_links = at_links.split("\n")
    id_list = ids_from_urls(at_links)
    st.write()

        
with output_ids:
    
    id_list = [f"'{id_}'" for id_ in id_list]
    
    code = f'''select distinct(ISRC), null as barcode, title, null as mix_name, artist, null as RD, label, label, label, distributor,'0' as price, identifier
from excep_dig_apple_master
where identifier in ({", ".join(id_list)})
order by identifier;'''
        
    st.code(code, language='sql')