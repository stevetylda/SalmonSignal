# ------------------------------------------------------- #
#                         MODULES                         #

# Standard Modules
import os

# Third-Party Modules
import pandas as pd
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


def get_filters_for_dam_data(dam_counts_df):
    column_list = ["DOY", "WOY", "MONTH", "DATE", "LOCATION", "SPECIES", "COUNT"]
    dam_counts_df = dam_counts_df[column_list]

    ### ----------------------
    ### Select X-Axis
    x_axis_ = st.multiselect(
        "Select Y-Axis",
        dam_counts_df.columns,
        max_selections=1,
        default=["DOY"],
    )
    x_axis_select = x_axis_[0]

    ### ----------------------
    ### Select Y-Axis
    y_axis_ = st.multiselect(
        "Select Y-Axis",
        ["COUNT", "DOY_ZSCORE"],
        max_selections=1,
        default=["COUNT", ],
    )
    y_axis_select = y_axis_[0]

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
            default=["DOY", "SPECIES"],
        )
        agg_options = set(agg_options)

        agg_func_option = st.selectbox(
            "Aggregation Function",
            ("Mean", "Median", "Sum", "Standard Deviation"),
        )

    else:
        agg_options = set(column_options_agg)

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
        plot_data = plot_data.groupby(agg_list, as_index=False)[y_axis_].mean()
    elif agg_func_option == "Median":
        plot_data = plot_data.groupby(agg_list, as_index=False)[y_axis_].median()
    elif agg_func_option == "Sum":
        plot_data = plot_data.groupby(agg_list, as_index=False)[y_axis_].sum()
    elif agg_func_option == "Standard Deviation":
        plot_data = plot_data.groupby(agg_list, as_index=False)[y_axis_].std()

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
dam_counts_df = pd.merge(dam_counts_df, dams, on=["DAM"])

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
    options=["Overview", "Analysis", "Modeling", "Background"],
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
            "Current State",
            "Abundance Insights",
            "Predation Insights",
            "Prey Insights",
            "Environmental Covariates",
        ]
    )

    ################################
    ## ANALYSIS - OVERVIEW

    with tabs[0]:
        st.header("Overview")
        st.markdown("---")

        st.write("Data Quality + Limitations")

    ################################
    ## ANALYSIS - ABUNDANCE INSIGHTS

    with tabs[1]:
        st.header("Abundance Insights")
        st.markdown("---")

        # ---------------------------- #
        #      DAM INVESTIGATION.      #

        st.subheader("Dam Investigation")
        st.caption("Change parameters below to investigate the data.")

        ### ----------------------
        ### Select Plotting Method
        option_map = {
            0: ":material/line_axis:",
            1: ":material/bar_chart:",
            2: ":material/area_chart:",
            3: ":material/database:",
        }
        plot_selection = st.segmented_control(
            "Tool",
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
                ) = get_filters_for_dam_data(dam_counts_df)

            agree = st.checkbox("Proceed with Plotting Dam Counts")

            if agree:
                # Plot Title - Dams
                plot_title = f"Columbia River Dam Analysis: Species by {', '.join(agg_options).title()} over {', '.join(x_axis_select).title()}"

                # Line Plot
                if plot_selection == 0:
                    dam_plot = plot_line_plot_columbia_dams(
                        plot_data, plot_title, x_axis_select, y_axis_select
                    )
                elif plot_selection == 1:
                    dam_plot = plot_bar_plot_columbia_dams(
                        plot_data, plot_title, x_axis_select, y_axis_select
                    )
                elif plot_selection == 2:
                    dam_plot = plot_area_plot_columbia_dams(
                        plot_data, plot_title, x_axis_select, y_axis_select
                    )

                st.plotly_chart(dam_plot, use_container_width=True)

        st.write("")

        st.markdown("---")

        st.subheader("Creel Reports")




        st.write("")

        st.markdown("---")

    ################################
    ## ANALYSIS - PREDATION INSIGHTS

    with tabs[2]:
        st.subheader("Predation Insights")
        st.write("Piniped")
        st.write("Harbor Seals")
        st.write("Stellar Sea Lion")
        st.write("California Sea Lion")
        st.write("Humans")
        st.write("Commercial Fishing")
        st.write("Recreational Fishing")
        st.write("Southern Resident Killer Whales (SRKW)")
        st.write("Transient Killer Whales (Biggs)")

    ################################
    ## ANALYSIS - PREY INSIGHTS

    with tabs[3]:
        st.subheader("Prey Availability")

    ################################
    ## ANALYSIS - ENVIRONMENTAL INSIGHTS

    with tabs[4]:
        st.subheader("Environmental Covariates")


###########################################################
## SUB-PAGE 3 - MODELING

elif current_page == "Modeling":
    st.title("Modeling")

###########################################################
## SUB-PAGE 4 - BACKGROUND

elif current_page == "Background":
    st.write("Background / Context modeling here...")


#                                                         #
# ------------------------------------------------------- #
