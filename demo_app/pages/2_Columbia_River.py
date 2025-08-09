# ------------------------------------------------------- #
#                         MODULES                         #

# Standard Modules
import os

# Third-Party Modules
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import geopandas as gpd
from streamlit.components.v1 import html
import plotly.express as px

# Built Modules
from src.utils import load_top_image_banner
from src.visuals import create_and_save_map

#                                                         #
# ------------------------------------------------------- #

# ------------------------------------------------------- #
#                         FUNCTIONS                       #


# Load Columbia River Spatial Layers
def load_columbia_river_data():
    # Define Pathing
    ## Marine Areas
    if os.path.exists("./data/processed/GIS/ocean/TERRITORIAL_COLUMBIA_MOUNT.parquet"):
        columbia_path = "./data/processed/GIS/ocean/TERRITORIAL_COLUMBIA_MOUNT.parquet"
    elif os.path.exists(
        "../data/processed/GIS/ocean/TERRITORIAL_COLUMBIA_MOUNT.parquet"
    ):
        columbia_path = "../data/processed/GIS/ocean/TERRITORIAL_COLUMBIA_MOUNT.parquet"
    else:
        st.write("PATHDOES NOT EXIST", os.getcwd())
        st.write(os.listdir())

    ## River Network
    if os.path.exists(
        "./data/processed/GIS/inland_waters/US_INLAND_WATERS_COLUMBIA_R.parquet"
    ):
        network_path = (
            "./data/processed/GIS/inland_waters/US_INLAND_WATERS_COLUMBIA_R.parquet"
        )
    elif os.path.exists(
        "../data/processed/GIS/inland_waters/US_INLAND_WATERS_COLUMBIA_R.parquet"
    ):
        network_path = (
            "../data/processed/GIS/inland_waters/US_INLAND_WATERS_COLUMBIA_R.parquet"
        )
    else:
        st.write("PATHDOES NOT EXIST", os.getcwd())
        st.write(os.listdir())

    ## Dam Locations
    if os.path.exists(
        "./data/processed/GIS/important_locations/columbia_snake_dams.parquet"
    ):
        dam_path = (
            "./data/processed/GIS/important_locations/columbia_snake_dams.parquet"
        )
    elif os.path.exists(
        "../data/processed/GIS/important_locations/columbia_snake_dams.parquet"
    ):
        dam_path = (
            "../data/processed/GIS/important_locations/columbia_snake_dams.parquet"
        )
    else:
        st.write("PATHDOES NOT EXIST", os.getcwd())
        st.write(os.listdir())

    # Data loading (unchanged)
    columbia_river_mouth = gpd.read_parquet(columbia_path).to_crs("EPSG:4326")
    river_gdf = gpd.read_parquet(network_path).to_crs("EPSG:4326")
    dams = gpd.read_parquet(dam_path).to_crs("EPSG:4326")

    return columbia_river_mouth, river_gdf, dams


# Load Dam Counts
def load_dam_counts(dam_count_directory):
    if os.path.exists(dam_count_directory):
        dam_counts_df = pd.read_parquet(dam_count_directory)

    elif os.path.exists(f"../{dam_count_directory}"):
        dam_counts_df = pd.read_parquet(f"../{dam_count_directory}")

    else:
        return st.write("DAM COUNTS UNAVAILABLE")

    # Standardize Columns
    dam_counts_df.columns = dam_counts_df.columns.str.upper()

    return dam_counts_df


#                                                         #
# ------------------------------------------------------- #

# ------------------------------------------------------- #
#                        PARAMETERS                       #

# Set page config to wide mode (must be first)
st.set_page_config(page_title="Columbia River Analysis", layout="wide")

# Dam Counts Direcotry - FPC
dam_count_directory = "./data/processed/FPC_DAM_COUNTS/"

DAM_COLORS = {
    "Bonneville": "#ef476f",
    "Dalles": "#ffd166",
    "John Day": "#06d6a0",
    "Willamette": "#118ab2",
    # Add more as needed
}

#                                                         #
# ------------------------------------------------------- #

# ------------------------------------------------------- #
#                         LOAD DATA                       #

# Load Spatial Layers
columbia_river_mouth, river_gdf, dams = load_columbia_river_data()

# Load Dam Counts
dam_counts_df = load_dam_counts(dam_count_directory)
dam_counts_df = pd.merge(dam_counts_df, dams, on=["DAM"])

#                                                         #
# ------------------------------------------------------- #

# ------------------------------------------------------- #
#                         BUILD PAGE                      #

# Title and banner
st.title("Columbia River - Salmon & Ecosystem Dynamics")
load_top_image_banner(top_image_path="hannah_smith_columbia.jpg")

# Sub-page selection
current_page = option_menu(
    menu_title=None,
    options=["Overview", "Analysis", "Modeling", "Background"],
    icons=["map", "graph-up", "layers", "eyeglasses"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# SUB-PAGE 1 - OVERVIEW
if current_page == "Overview":
    st.subheader("Analysis Area")

    # Inject CSS to force full-width rendering
    st.markdown(
        """
        <style>
            /* Reset Streamlit container styles */
            .block-container, .main, .stApp, div[data-testid="stHorizontalBlock"], 
            div[data-testid="stTabs"], div[role="tabpanel"], .stHorizontal, .element-container {
                max-width: 100% !important;
                width: 100% !important;
                padding: 1 !important;
                margin: 1 !important;
                overflow: visible !important;
            }
            /* Ensure map and its container are full-width */
            .leaflet-container, .folium-map, [id^="map_"] {
                width: 100% !important;
                height: 600px !important;
                margin: 1 !important;
                padding: 1 !important;
                position: relative !important;
            }
            /* Override flexbox or grid constraints */
            div[data-testid="stHorizontalBlock"] > div, div[data-testid="stTabs"] > div,
            .stHorizontal > div {
                flex: 1 1 100% !important;
                width: 100% !important;
                max-width: 100% !important;
            }
            /* Ensure the wrapper div is full-width */
            .map-wrapper {
                width: 100vw !important;
                max-width: 100% !important;
                height: 600px !important;
                margin: 1 !important;
                padding: 1 !important;
                overflow: hidden !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Create or load Folium map
    output_file = create_and_save_map(
        columbia_river_mouth, river_gdf, dams, force_regenerate=False
    )

    # Read the map HTML
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            map_html = f.read()
    except Exception as e:
        st.error(f"Error reading map.html: {e}")
        st.write("Regenerating map...")
        output_file = create_and_save_map(
            columbia_river_mouth, river_gdf, dams, force_regenerate=True
        )
        with open(output_file, "r", encoding="utf-8") as f:
            map_html = f.read()

    # Inject CSS for Leaflet's map container
    css_fix = """
    <style>
    /* Force leaflet map container inside folium HTML to fill parent div */
    #map { height: 100% !important; width: 100% !important; }
    html, body { margin: 0; padding: 0; height: 100%; width: 100%; }
    </style>
    """

    container = f"""
    <div style="width: 100vw; min-width: 600px; height: 600px; margin: 0; padding: 0;">
    {css_fix}
    {map_html}
    </div>
    """

    # Render the map
    html(container, height=600)

elif current_page == "Analysis":
    st.title("Salmon Metrics - Columbia River Analysis")
    tabs = st.tabs(
        [
            "Current State",
            "Abundance Insights",
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
        st.write("Abundance Insights")
        st.markdown("---")

        st.write("Dam Investigation")

        # Sample toggles for color
        species_options = sorted(list(dam_counts_df.SPECIES.unique()))
        species_choice = st.radio("Select Species:", species_options)

        color_options = ["Count", "Normalized Count"]
        color_choice = st.radio("Color points by:", color_options)

        def plot_plotly_mapbox_time_series(df, color_choice, species_choice):
            if color_choice == "Normalized Count":
                color_plot = "DOY_ZSCORE"
            else:
                color_plot = "COUNT"

            df = df[df.SPECIES == species_choice]

            fig = px.scatter_mapbox(
                df,
                lat="LAT",
                lon="LON",
                color=color_plot,
                hover_name="LOCATION",
                size=[10] * len(df),
                hover_data={
                    "DATE": True,
                    "DAM": False,
                    "COUNT": True,
                    "DOY_ZSCORE": True,
                    "LAT": False,
                    "LON": False,
                },
                zoom=6,
                height=600,
                title="Map - Displaying Count of Salmon at Dams Along the Columbia",
                animation_frame="DATE",
                color_continuous_scale="RdBu",  # Red-Blue diverging color scale # or your custom palette
            )

            # Center the diverging color scale on zero
            fig.update_traces(marker=dict(colorscale="RdBu", showscale=True))

            fig.update_layout(
                mapbox_style="open-street-map",
                margin={"r": 0, "t": 30, "l": 0, "b": 0},
                coloraxis_colorbar=dict(
                    title=color_choice,  # Title for the color scale
                    tickvals=[
                        -max(df[color_plot].abs()),
                        0,
                        max(df[color_plot].abs()),
                    ],
                    ticktext=[
                        f"-{max(df[color_plot].abs())}",
                        "0",
                        f"{max(df[color_plot].abs())}",
                    ],
                ),
            )

            return fig

        # fig_ts_mapbox = plot_plotly_mapbox_time_series(
        #     dam_counts_df, color_choice, species_choice
        # )
        # st.plotly_chart(fig_ts_mapbox, use_container_width=True)

        st.markdown("---")
        st.write("Dam Counts")

        # 2. Multi-select Dam filter with a "Select All" helper
        all_dams = list(DAM_COLORS.keys())

        # Use colored_options as both options and default:
        selected_dams = st.multiselect(
            "Select Dam(s)",
            options=all_dams,
            default=all_dams,  # select all by default
        )

        # 3. Filter the dataframe based on selection
        filtered_df = dam_counts_df[dam_counts_df["LOCATION"].isin(selected_dams)]

        # 4. Aggregate counts by date and dam (if you want sum across species, just remove species filter)
        agg_df = filtered_df.groupby(["DATE", "LOCATION"], as_index=False)[
            "COUNT"
        ].sum()

        # 5. Make the Plotly time series plot
        fig = px.line(
            agg_df,
            x="DATE",
            y="COUNT",
            color="LOCATION",
            color_discrete_map=DAM_COLORS,
            title="Fish Counts by Dam Over Time",
            labels={"DATETIME": "Date", "COUNT": "Count", "LOCATION": "Dam Location"},
        )

        fig.update_layout(legend_title_text="Dam Location")

        fig.update_layout(
            plot_bgcolor="white",  # white plot area
            paper_bgcolor="white",  # white outside plot
            font=dict(family="Segoe UI, Arial, sans-serif", size=12, color="black"),
            xaxis=dict(
                showgrid=True,
                gridcolor="lightgray",
                zeroline=False,
                showline=True,
                linecolor="black",
                ticks="outside",
                tickcolor="black",
                ticklen=5,
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="lightgray",
                zeroline=False,
                showline=True,
                linecolor="black",
                ticks="outside",
                tickcolor="black",
                ticklen=5,
            ),
            legend=dict(
                bgcolor="rgba(255,255,255,0.8)",  # white with slight transparency
                bordercolor="lightgray",
                borderwidth=1,
                font=dict(size=11),
                x=1.02,
                y=1,
                xanchor="left",
                yanchor="top",
            ),
            margin=dict(l=50, r=50, t=50, b=50),
        )
        fig.update_layout(
            title=dict(
                text="Fish Counts by Dam Over Time",
                font=dict(color="black", size=18, family="Segoe UI, Arial, sans-serif"),
                x=0.5,  # center title
            ),
            xaxis=dict(
                title=dict(text="Date", font=dict(color="black", size=14)),
                tickfont=dict(color="black"),
                showgrid=True,
                gridcolor="lightgray",
                zeroline=False,
                showline=True,
                linecolor="black",
                ticks="outside",
                tickcolor="black",
                ticklen=5,
            ),
            yaxis=dict(
                title=dict(text="Count", font=dict(color="black", size=14)),
                tickfont=dict(color="black"),
                showgrid=True,
                gridcolor="lightgray",
                zeroline=False,
                showline=True,
                linecolor="black",
                ticks="outside",
                tickcolor="black",
                ticklen=5,
            ),
            legend=dict(
                title=dict(text="Dam Location", font=dict(color="black", size=12)),
                font=dict(color="black", size=11),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="lightgray",
                borderwidth=1,
                x=1.02,
                y=1,
                xanchor="left",
                yanchor="top",
            ),
        )

        # 6. Show the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        st.write("do consistent colors by dam, consistent colors by species")
        st.write(
            "filter to species, date range, dam - if you select multiple shwo them as individual colors"
        )

        st.write("Creel Reports")

        st.write("")

        st.markdown("---")

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

elif current_page == "Modeling":
    st.title("Modeling")

# Other sub-pages (unchanged)
elif current_page == "Background":
    st.write("Background / Context modeling here...")


#                                                         #
# ------------------------------------------------------- #
