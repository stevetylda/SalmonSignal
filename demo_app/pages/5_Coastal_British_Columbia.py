import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_folium import st_folium
from src.utils import load_top_image_banner

# Page Parameters
page_tab_title = "Coastal California Analysis"
page_name = "Coastal California - Coming Soon!"
page_title = "Coastal California - Salmon & Ecosystem Dynamics"
top_image_path = "sergey-pesterev_bc_coast.jpg"

# Set Page Parameters
st.set_page_config(page_title=page_tab_title, layout="wide")
st.title(page_title)

st.markdown(
    """
    <style>
    .shaded-box {
        background-color: #f6f8f9;  /* light slate fog */
        padding: 2rem;
        border-radius: 12px;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);  /* subtle shadow */
    }

    /* You can reuse your gif-container or other styles inside this */
    </style>
""",
    unsafe_allow_html=True,
)

# Load Top Image
load_top_image_banner(top_image_path=top_image_path)

# Load Material Symbols globally
st.markdown(
    """
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# CSS
st.markdown(
    """
    <style>
    .shaded-box {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 12px;
        margin-top: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    }

    .section-title {
        font-size: 2.5rem;
        font-weight: 600;
        color: #ffffff;
        text-align: center;
        margin-bottom: 1rem;
        margin-top: 0;
    }

    .coming-soon {
        font-size: 1.8rem;
        font-weight: 500;
        color: #f0f0f0; 
        text-align: center;
        margin: 0.5rem 0 0;
    }

    .material-symbols-outlined {
        font-family: 'Material Symbols Outlined';
        font-variation-settings:
          'FILL' 0,
          'wght' 400,
          'GRAD' 0,
          'opsz' 48;
        vertical-align: middle;
        font-size: 1.4em;
        margin: 0 0.3em;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Shaded box with header + coming soon
st.markdown(
    f"""
    <div class="shaded-box">
        <div class="section-title">{page_title}</div>
        <hr>
        <div class="coming-soon">
            <span class="material-symbols-outlined">construction</span>
            {page_name}
            <span class="material-symbols-outlined">construction</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
