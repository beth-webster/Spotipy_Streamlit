import streamlit as st
import re

# Functions
def ids_from_urls(at_links):
    
    url_id_map = {}
    
    for url in at_links:        
        try:
            url_regex = re.search(r"(?<=i=)\d+", url)            
            if url_regex:
                url_id_map[url] = url_regex.group()
                
        except AttributeError:
            url_id_map[url] = 'invalid input'
            
    return url_id_map

# Set page configuration to wide for primary desktop use
st.set_page_config(layout="wide")

# Create dashboard sections
header = st.container()
links_input = st.container()
output_ids = st.container()
compare_ids = st.container()

# Header Sction of page
with header:
    st.write("Extract IDs from iTunes links, add into code & compares output IDs for email back!")
    
# Main page section
with links_input:
    
    at_links = st.text_area('Paste links here')
    at_links = at_links.split("\n")
    url_id_map = ids_from_urls(at_links)
    id_list = list(url_id_map.values())
    st.write()

        
with output_ids:
    
    id_list_code = [f"'{id_}'" for id_ in id_list]
    
    code = f'''select distinct(ISRC), null as barcode, title, null as mix_name, artist, null as RD, label, label, label, distributor,'0' as price, identifier
from excep_dig_apple_master
where identifier in ({", ".join(id_list_code)})
order by identifier;'''
        
    st.code(code, language='sql')
    
with compare_ids:
    
    output_ids = st.text_area('Paste output IDs here')
    output_ids = output_ids.split("\n")
    missing_urls = [url for url, id_ in url_id_map.items() if id_ not in output_ids]
    missing_urls_out = '\n'.join(missing_urls)
    
    st.code(f"""Hope you are well! 
\nThese have been added and flagged, with the exception of the below:
\n{missing_urls_out}""", language = 'csv')