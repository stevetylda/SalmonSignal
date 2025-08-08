import streamlit as st
from streamlit_option_menu import option_menu
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Set Page Parameters
st.set_page_config(page_title="Columbia River Analysis", layout="wide")

# Set Page Title
st.title("Columbia River - Salmon & Ecosystem Dynamics")

# Get Sub-Page Selection
current_page = option_menu(
    menu_title=None,
    options=["Overview", "Analysis", "Modeling", "Background"],
    icons=["map", "graph-up", "layers", "eyeglasses"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

#########################################################################
# SUB-PAGE 1 - OVERVIEW
if current_page == "Overview":
    st.write("Overview content here...")

#                                                                       #
#########################################################################

#########################################################################
# SUB-PAGE 2 - OVERVIEW
elif current_page == "Background":
    st.write("Background / Context modeling here...")

#                                                                       #
#########################################################################

#########################################################################
# SUB-PAGE 3 - ANALYSIS
elif current_page == "Analysis":
    st.title("Salmon Metrics - Columbia River Analysis")

    # Tabs for different analyses
    tabs = st.tabs(
        [
            "Overview",
            "Abundance",
            "Predation Insights",
            "Prey Insights",
            "Environmental Covariates",
        ]
    )

    with tabs[0]:
        st.write("Overview")

        st.markdown("---")
        st.write("Data Quality + Limitations")

    with tabs[1]:
        st.write("Abundance")

        # Dams

        # Creel Reports

    with tabs[2]:
        st.title("Predation Insights")
        st.write("Piniped")
        st.write("Harbor Seals")
        st.write("Stellar Sea Lion")
        st.write("California Sea Lion")
        st.write("Humans")
        st.write("Commercial Fishing")
        st.write("Recreational Fishing")

        st.write("Southern Resident Killer Whales (SRKW)")

        st.write("Transient Killer Whales (Biggs)")

    with tabs[3]:
        st.write("Prey Availability")

    with tabs[4]:
        st.write("Environmental Covariates")

#                                                                       #
#########################################################################

#########################################################################
# SUB-PAGE 4 - MODELING
elif current_page == "Modeling":
    st.title("Modeling")
