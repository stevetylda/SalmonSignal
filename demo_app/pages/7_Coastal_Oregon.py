import streamlit as st
from streamlit_option_menu import option_menu
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Set Page Parameters
st.set_page_config(page_title="Oregon Coastal Analysis", layout="wide")

# Set Page Title
st.title("Oregon Coast - Salmon & Ecosystem Dynamics")
