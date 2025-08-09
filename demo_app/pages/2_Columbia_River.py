# ------------------------------------------------------- #
#                         MODULES                         #

# Standard Modules
import os

# Third-Party Modules
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import geopandas as gpd

import plotly.express as px

# Built Modules
## Import Parameters
from config.color_config import DAM_COLORS, SPECIES_COLORS

## Import Functions
from src.utils import load_top_image_banner
from src.visuals import (
    plot_overview_map_columbia,
    plot_line_plot_columbia_dams,
    plot_bar_plot_columbia_dams,
    plot_area_plot_columbia_dams,
)

from src.auth import check_password_user

if not check_password_user():
    st.stop()

#                                                         #
# ------------------------------------------------------- #

# ------------------------------------------------------- #
#                         FUNCTIONS                       #


# Load Columbia River Spatial Layers
@st.cache_data
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
@st.cache_data
def load_dam_counts(dam_count_directory):
    if os.path.exists(dam_count_directory):
        dam_counts_df = pd.read_parquet(dam_count_directory)

        # Standardize Columns
        dam_counts_df.columns = dam_counts_df.columns.str.upper()

    elif os.path.exists(f"../{dam_count_directory}"):
        dam_counts_df = pd.read_parquet(f"../{dam_count_directory}")

        # Standardize Columns
        dam_counts_df.columns = dam_counts_df.columns.str.upper()

    else:
        return st.write("DAM COUNTS UNAVAILABLE")

    return dam_counts_df


def get_filters_for_dam_data(dam_counts_df):
    column_list = [
        "DOY",
        "WOY",
        "MONTH",
        "YEAR",
        "YEAR_MONTH",
        "DATE",
        "LOCATION",
        "SPECIES",
        "COUNT",
        "DOY_ZSCORE",
    ]
    dam_counts_df = dam_counts_df[column_list]

    ### ----------------------
    ### Select X-Axis
    x_axis_select = st.selectbox(
        "Select X-Axis",
        options=["DOY"]
        + [i for i in dam_counts_df.columns if i not in ["COUNT", "DOY_ZSCORE", "DOY"]],
        index=0,
    )

    ### ----------------------
    ### Select Y-Axis
    y_axis_select = st.selectbox(
        "Select Y-Axis", options=["COUNT", "DOY_ZSCORE"], index=0
    )

    ### ----------------------
    ### Select Aggregate Data?
    aggregate = st.toggle("Aggregate Data?", value=True)

    ### ----------------------
    ### Select Aggregater Cols
    column_options_agg = list(
        set(dam_counts_df.columns) - set(["LAT", "LON", "TYPE", "geometry"])
    )

    if aggregate == True:
        agg_options = st.multiselect(
            "Select Level of Aggregation",
            column_options_agg,
            default=["SPECIES"],
        )
        agg_options = set(agg_options)

        agg_func_option = st.selectbox(
            "Aggregation Function",
            ("Mean", "Median", "Sum", "Standard Deviation"),
        )

        color_by_agg_option = st.selectbox(
            "Color by Aggregation?",
            list(agg_options),
        )

    else:
        agg_options = set(column_options_agg)
        color_by_agg_option = None

    ### ----------------------
    ### Select Aggregate Data?
    data_filter = st.toggle("Filter Data?", value=False)

    ## Select Species
    species_options = sorted(list(dam_counts_df.SPECIES.unique()))

    # Select Dams
    dam_options = sorted(list(dam_counts_df.LOCATION.unique()))

    if data_filter == True:
        # Species Select
        selected_species = st.multiselect(
            "Select Species",
            species_options,
            default=species_options,
        )
        # Dam Select
        selected_dams = st.multiselect(
            "Select Location",
            dam_options,
            default=dam_options,
        )
    else:
        selected_species = species_options
        selected_dams = dam_options

    # Prepare Data for Plot
    ## Subset Columbs
    column_list = list(
        set(["LOCATION", "SPECIES", y_axis_select, x_axis_select]) | agg_options
    )
    plot_data = dam_counts_df[column_list]

    ## Filter Data
    plot_data = plot_data[
        (plot_data.SPECIES.isin(selected_species))
        & (plot_data.LOCATION.isin(selected_dams))
    ]

    ## Aggregate
    agg_list = list(set([x_axis_select]) | agg_options)

    if agg_func_option == "Mean":
        plot_data = plot_data.groupby(agg_list, as_index=False)[y_axis_select].mean()
    elif agg_func_option == "Median":
        plot_data = plot_data.groupby(agg_list, as_index=False)[y_axis_select].median()
    elif agg_func_option == "Sum":
        plot_data = plot_data.groupby(agg_list, as_index=False)[y_axis_select].sum()
    elif agg_func_option == "Standard Deviation":
        plot_data = plot_data.groupby(agg_list, as_index=False)[y_axis_select].std()

    plot_data = plot_data.sort_values(x_axis_select)
    plot_data = plot_data.reset_index(drop=True)

    # Build UID for Plotting
    col_for_uid = list(agg_options - set([y_axis_select, x_axis_select]))

    plot_data["UID"] = plot_data[col_for_uid].astype(str).agg("-".join, axis=1)

    return (
        plot_data,
        selected_species,
        selected_dams,
        x_axis_select,
        y_axis_select,
        agg_options,
        color_by_agg_option,
    )


#                                                         #
# ------------------------------------------------------- #

# ------------------------------------------------------- #
#                        PARAMETERS                       #

# Set page config to wide mode (must be first)
st.set_page_config(page_title="Columbia River Analysis", layout="wide")

# Dam Counts Direcotry - FPC
dam_count_directory = "./data/processed/FPC_DAM_COUNTS/"

#                                                         #
# ------------------------------------------------------- #

# ------------------------------------------------------- #
#                         LOAD DATA                       #

# Load Spatial Layers
columbia_river_mouth, river_gdf, dams = load_columbia_river_data()

# Load Dam Counts
dam_counts_df = load_dam_counts(dam_count_directory)
dam_counts_df = pd.merge(dam_counts_df, dams.drop(columns=["geometry"]), on=["DAM"])

#                                                         #
# ------------------------------------------------------- #

# ------------------------------------------------------- #
#                         BUILD PAGE                      #

###########################################################
## PAGE HEADER

# Set Page Title
st.title("Columbia River - Salmon & Ecosystem Dynamics")

# Load Banner Image
load_top_image_banner(top_image_path="hannah_smith_columbia.jpg")

# Sub-page selection
current_page = option_menu(
    menu_title=None,
    options=["Overview", "Analysis", "Modeling", "Sources + Methods"],
    icons=["map", "graph-up", "layers", "eyeglasses"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

###########################################################
## SUB-PAGE 1 - OVERVIEW

if current_page == "Overview":
    st.subheader("Analysis Area")

    # Plot Overview Map
    plot_overview_map_columbia(columbia_river_mouth, river_gdf, dams)

    st.write("TODO: add haul-out locations by species, add boat ramps, add ruler")
    st.write("TODO: add legend, ")
    st.write("TODO: add description for what this section is about")

###########################################################
## SUB-PAGE 2 - ANALYSIS

elif current_page == "Analysis":
    ################################
    ## ANALYSIS - HEADER

    # Page Title
    st.title("Salmon Metrics - Columbia River Analysis")

    # Tab Options
    tabs = st.tabs(
        [
            "Analysis - Overview",
            "Salmon Abundance & Trends",
            "Predation Dynamics",
            "Prey Availability",
            "Environmental Drivers",
            "Bringing It All Together",
        ]
    )

    ################################
    ## ANALYSIS - OVERVIEW

    with tabs[0]:
        st.header("Analysis - Overview")
        st.markdown("---")

        st.markdown(
            """
            Welcome to the Analysis Section — your central hub for exploring salmon availability in the Columbia River ecosystem and its vital connection to both Southern Resident Killer Whales (SRKW) and transient orca populations.
            Salmon serve as a primary prey source for these apex predators, while their presence and movements also influence the distribution and behavior of orcas by attracting the orcas’ own prey.
            This section is organized into five key areas, each offering in-depth insights into the factors that influence salmon populations and their surrounding environment.
            Together, these views provide a comprehensive picture of the complex natural rhythms shaping salmon life and their role in the orca food web.
            """
        )

        tab_list = {
            "Abundance Insights": "Dive into detailed salmon population data, including seasonal fluctuations, spatial distribution, and historical trends. This section helps track how salmon numbers ebb and flow across the river system, highlighting periods of abundance and scarcity that are crucial for understanding salmon dynamics over time.",
            "Predation Insights": "Examine the impact of predation on salmon populations by analyzing sighting records, behavioral data, and predation pressure from species such as orcas, seals, and human fishing activities. This section sheds light on predator-prey interactions and how these relationships affect salmon survival rates and movement patterns.",
            "Prey Insights": "Understand the availability and distribution of prey species that salmon depend on throughout their life cycle. This section explores the abundance of forage fish and other food sources, helping to reveal how prey dynamics influence salmon growth, health, and migration success.",
            "Environmental Indicators": "Explore critical environmental variables like water temperature, river flow, dissolved oxygen levels, and habitat conditions. These indicators play a fundamental role in salmon physiology and behavior, shaping migration timing, spawning success, and overall ecosystem health.",
            "Bringing It All Together": "Integrate data from abundance, predation, prey, and environmental factors into unified visualizations and summaries. This section highlights the interconnected nature of these drivers and supports a more nuanced understanding of salmon ecosystem dynamics.",
        }

        for title, desc in tab_list.items():
            st.markdown(f"### {title}\n{desc}")

        st.markdown(
            """
            ---
            **How to Use This Section:**  
            Take your time exploring each area to uncover the multiple layers influencing salmon availability and how these patterns relate to both resident and transient orca populations.
            Salmon are not only key prey themselves but also influence the presence of other species that orcas may hunt.
            This space invites curiosity and thoughtful analysis, encouraging you to connect different data streams and build a richer understanding of the intricate ecological relationships within the Columbia River ecosystem.
            """
        )

        st.markdown(
            """
            ---
            _Data sources include regional fish counts, predator observations, environmental monitoring programs, and more._  
            """
        )

        st.write(
            "^ this more should be a link to a table or an additional webpage or something that references the data sources... "
        )

    ################################
    ## ANALYSIS - ABUNDANCE INSIGHTS

    with tabs[1]:
        st.header("Salmon Abundance & Trends")
        st.markdown("---")

        # ---------------------------- #
        #      DAM INVESTIGATION.      #

        st.subheader("Dam Investigation")
        # st.caption("Change parameters below to investigate the data.")
        # Data from here: https://www.fpc.org/web/apps/adultsalmon/R_adultcount_dataquery_results.php

        ### ----------------------
        ### Select Plotting Method
        option_map = {
            0: ":material/line_axis:",
            1: ":material/bar_chart:",
            2: ":material/area_chart:",
            3: ":material/database:",
        }
        plot_selection = st.segmented_control(
            "Change parameters below to investigate the data.",
            options=option_map.keys(),
            format_func=lambda option: option_map[option],
            selection_mode="single",
        )

        # Show Table
        if plot_selection == 3:
            st.table(dam_counts_df.head(25))

        # Allow for Data Analysis
        elif plot_selection is not None:
            # Data Selection for Plots
            with st.expander("Data Selection"):
                (
                    plot_data,
                    selected_species,
                    selected_dams,
                    x_axis_select,
                    y_axis_select,
                    agg_options,
                    color_by_agg_option,
                ) = get_filters_for_dam_data(dam_counts_df)

            agree = st.checkbox("Proceed with Plotting Dam Counts")

            if agree:
                # Plot Title - Dams
                plot_title = f"Columbia River Dam Analysis: SPECIES by {', '.join(agg_options).upper()} over {x_axis_select.upper()}"

                # Line Plot
                if plot_selection == 0:
                    dam_plot = plot_line_plot_columbia_dams(
                        plot_data,
                        plot_title,
                        x_axis_select,
                        y_axis_select,
                        color_by_agg_option,
                    )
                elif plot_selection == 1:
                    dam_plot = plot_bar_plot_columbia_dams(
                        plot_data,
                        plot_title,
                        x_axis_select,
                        y_axis_select,
                        color_by_agg_option,
                    )
                elif plot_selection == 2:
                    dam_plot = plot_area_plot_columbia_dams(
                        plot_data,
                        plot_title,
                        x_axis_select,
                        y_axis_select,
                        color_by_agg_option,
                    )

                st.plotly_chart(dam_plot, use_container_width=True)

        st.write("")

        st.markdown("---")

        st.subheader("Creel Reports")

        st.write("")

        st.markdown("---")

        st.subheader("Catch Card Reports")

        st.write("")

        st.markdown("---")

        st.subheader("Smolt Outmigration")

        st.write("")

        st.markdown("---")

        st.subheader("Genetic Origin Data")

        st.write("")

        st.markdown("---")

        st.subheader("Recovery / Catch Data")

        st.write("")

        st.markdown("---")

        st.subheader("Release Data")

        st.write("")

        st.markdown("---")

    ################################
    ## ANALYSIS - PREDATION INSIGHTS

    with tabs[2]:
        st.header("Predation Dynamics")
        st.markdown("---")

        # ---------------------------- #
        #  KILLER WHALE INVESTIGATION  #

        st.subheader("Killer Whale Investigation - Residents, Transients (Biggs)")

        # Filters will include buffer distance from mouth of columbia

        # Filter to Species Type

        # We need a custom coloring scheme

        # Time series plot of counts over time

        st.write("Southern Resident Killer Whales (SRKW)")
        st.write("Transient Killer Whales (Biggs)")

        st.write("")
        st.markdown("---")

        # ---------------------------- #
        #     PINNIPED INVESTIGATION   #

        st.subheader(
            "Pinniped Investigation - California Sea Lions (CSL), Stellar Sea Lions (SSL), Harbour Seals"
        )

        st.write("")
        st.markdown("---")

        # ---------------------------- #
        #      HUMAN INVESTIGATION     #

        st.subheader(
            "Human Investigation - Population Density, Built-Up Area, Docks/Ramps, Recreational Fishing, Commercial Fishing"
        )

        st.write("")
        st.markdown("---")

    ################################
    ## ANALYSIS - PREY INSIGHTS

    with tabs[3]:
        st.subheader("Prey Availability")

        st.write(
            "need to actually find data for this for it to become relevant to this analysis."
        )

    ################################
    ## ANALYSIS - ENVIRONMENTAL INSIGHTS

    with tabs[4]:
        st.subheader("Environmental Drivers")

        st.write("River Temps (DayTime vs. NightTime)")
        st.write("Flow")
        st.write("Depth")
        st.write(
            "Weather-Related Variables (e.g., cloud cover, rainfall, weather events)"
        )
        st.write("Tides")
        st.write("Lunar Intensity")
        st.write("Human Population Density")

    ################################
    ## ANALYSIS - INTEGRATED ECOSYSTEM

    with tabs[5]:
        st.subheader("Integrated Ecosystem View")

        st.write(
            "here we could put plots that bring all of this time series data together or correlation analysis"
        )

        st.write(
            "here we could put a grid-based map to show what these variables look like over spatiallly... "
        )


###########################################################
## SUB-PAGE 3 - MODELING

elif current_page == "Modeling":
    st.title("Modeling")

    ##########################

    st.subheader(
        "Model 1- Chained Logic: Temporally-Bound Estimation of Salmon Density Along Columbia River"
    )
    st.write(
        "drop proxies map of dam-to-dam distances and connections, we need to show flow of species from location to location to be able to estimate abundance at the mouth of the Pacific"
    )
    st.write(
        "the hypothesis would be that SRKWs are around the mouth when abundance is historically high (relative to food availability elsewhere and based on historical knowledge of abundance patterns) - we may not have a direct estimate of this abundance, but we have many covariates that we can measure and we have counts at most dams since the 1950s which could give insight on salmon movement counts, which we could back estimate to a Columbia mouth abundance n-timesteps prior to Bonneville/Willametter abundance counts"
    )
    st.write(
        "add modeling methodology for salmon movement - adult, juvenille, jack, other fish"
    )
    st.write(
        "add modeling variable includer - given list of x (dropdown select many), predict y  (y is relative abundance of salmon fish)"
    )
    st.write(
        "show how we back trace this estimate to the Pacific to show salmon abundance off shore and around the mouth of the Columbia"
    )
    st.write("add tools for traceability...")
    st.write("show Orca sightings map relative to this... ")

    ##########################

    st.subheader(
        "Model 2 - Adult Salmon Forecasting System: Estimate Return Window of Salmon to Columbia"
    )

    st.write(
        "once we have a sufficient estimate at the mouth of the Columbia, we should see if we can identify indicators from the ocean, time of year, etc... that would indicate a return time window for next year returns"
    )

    ##########################

    st.subheader(
        "Model 3 - Juvenille Salmon Forecasting System: Estimate Dispersion of Juvenille Salmon to the Pacific along the Columbia"
    )

    st.write(
        "we need to find data to support this... but this will only add to the abundance estimates along the Columbia"
    )


###########################################################
## SUB-PAGE 4 - BACKGROUND

elif current_page == "Sources + Methods":
    st.write("Background / Context modeling here...")


#                                                         #
# ------------------------------------------------------- #
