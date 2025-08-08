import streamlit as st
from streamlit_option_menu import option_menu
import geopandas as gpd
import folium
import os
from streamlit_folium import st_folium

# Set Page Parameters
st.set_page_config(page_title="Ballard Locks Analysis", layout="wide")

st.markdown(
    """
    <style>
    img {
        height: 125px !important;
        object-fit: cover;
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if os.path.exists("./demo_app/assets/tinibias_ballard_image.jpg"):
    st.image("./demo_app/assets/tinibias_ballard_image.jpg")
elif os.path.exists("./../demo_app/assets/tinibias_ballard_image.jpg"):
    st.image("./../demo_app/assets/tinibias_ballard_image.jpg")

# Set Page Title
st.title("Ballard Locks - Salmon & Ecosystem Dynamics")
