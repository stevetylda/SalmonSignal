# ------------------------------------------------------- #
#                         MODULES                         #

# Standard Modules
import os

# Third-Party Modules
import folium
import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.colors as mcolors
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from shapely.geometry import mapping
from streamlit.components.v1 import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors


#                                                         #
# ------------------------------------------------------- #

# ------------------------------------------------------- #
#                        FUNCTIONS                        #

#############################
## COLUMBIA RIVER - OVERVIEW


def plot_overview_map_columbia(columbia_river_mouth, river_gdf, dams):
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


#############################
## COLUMBIA RIVER ANALYSIS


# Function to create and save Folium map
def create_and_save_map(columbia_river_mouth, river_gdf, dams, force_regenerate=False):
    output_path = "map.html"
    if force_regenerate or not os.path.exists(output_path):
        color_map = {"MAJOR": "#084594", "MINOR": "#deebf7"}
        m = folium.Map(
            location=[47.4, -120.5], zoom_start=6.5, tiles="CartoDB Positron"
        )
        major_group = folium.FeatureGroup(name="Major Rivers", show=True)
        for _, row in river_gdf[river_gdf["RIVER_TYPE"] == "MAJOR"].iterrows():
            folium.GeoJson(
                mapping(row.geometry),
                style_function=lambda x: {
                    "fillColor": color_map["MAJOR"],
                    "color": color_map["MAJOR"],
                    "weight": 2,
                    "fillOpacity": 0.7,
                },
            ).add_to(major_group)
        major_group.add_to(m)
        minor_group = folium.FeatureGroup(name="Minor Rivers", show=False)
        for _, row in river_gdf[river_gdf["RIVER_TYPE"] == "MINOR"].iterrows():
            folium.GeoJson(
                mapping(row.geometry),
                style_function=lambda x: {
                    "fillColor": color_map["MINOR"],
                    "color": color_map["MINOR"],
                    "weight": 1,
                    "fillOpacity": 0.3,
                },
            ).add_to(minor_group)
        minor_group.add_to(m)
        for _, row in columbia_river_mouth.iterrows():
            if row["geometry"] and not row["geometry"].is_empty:
                folium.GeoJson(
                    mapping(row["geometry"]),
                    name="Marine Area",
                    style_function=lambda x: {
                        "fillColor": "#a6bddb",
                        "color": "#3690c0",
                        "weight": 1,
                        "fillOpacity": 0.4,
                    },
                    tooltip="Marine Area",
                ).add_to(m)
        dam_group = folium.FeatureGroup(name="Dams", show=True)
        for _, row in dams.iterrows():
            if row.geometry.geom_type == "Point":
                folium.Marker(
                    location=[row.geometry.y, row.geometry.x],
                    tooltip=row.get("NAME", "Dam"),
                    icon=folium.Icon(
                        icon="house-flood-water",
                        prefix="fa",
                        color="blue",
                        icon_color="white",
                    ),
                ).add_to(dam_group)
        dam_group.add_to(m)
        folium.LayerControl().add_to(m)
        m.save(output_path)
    return output_path


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


def create_continuous_cmap(colors, n_colors=50):
    """
    Create a continuous color map with n_colors from a list of hex colors.

    Args:
        colors (list): List of hex color codes
        n_colors (int): Number of colors to interpolate (default: 50)

    Returns:
        list: List of n_colors hex color codes
    """
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors, N=n_colors)
    return [mcolors.to_hex(cmap(i / (n_colors - 1))) for i in range(n_colors)]


def plot_area_plot_columbia_dams(
    plot_data, plot_title, x_axis_select, y_axis_select, color_by_agg_option=None
):
    """
    Create an area plot for Columbia dams data with dynamic color scaling, sorting areas by total size (smallest in front).

    Args:
        plot_data (pd.DataFrame): Input DataFrame with columns including UID, x_axis_select, y_axis_select
        plot_title (str): Title of the plot
        x_axis_select (str): Column name for x-axis
        y_axis_select (str): Column name for y-axis
        color_by_agg_option (str, optional): Aggregation option to color by (numeric or categorical)
    """
    if not isinstance(plot_data, pd.DataFrame):
        raise ValueError("plot_data must be a pandas DataFrame")
    if x_axis_select not in plot_data.columns or y_axis_select not in plot_data.columns:
        raise ValueError("Selected axis columns must exist in the DataFrame")
    if "UID" not in plot_data.columns:
        raise ValueError("DataFrame must contain 'UID' column")

    # Handle YEAR_WEEK format if used
    if x_axis_select == "YEAR_WEEK":
        plot_data = plot_data.copy()
        plot_data[x_axis_select] = pd.to_datetime(
            plot_data[x_axis_select] + "-0", format="%Y-%U-%w", errors="coerce"
        )

    numeric_agg_options = ["DATE", "DOY", "WOY", "MONTH", "YEAR"]
    categorical_agg_options = ["SPECIES", "DAM", "LOCATION"]

    # Sort data by color_by_agg_option and x_axis_select if provided
    if color_by_agg_option is not None:
        plot_data = plot_data.sort_values([color_by_agg_option, x_axis_select])
    else:
        plot_data = plot_data.sort_values(x_axis_select)
    plot_data = plot_data.reset_index(drop=True)

    # Calculate total y_axis_select values for each UID to sort areas (smallest in front)
    uid_totals = plot_data.groupby("UID")[y_axis_select].sum().reset_index()
    uid_totals = uid_totals.sort_values(
        y_axis_select, ascending=False
    )  # Descending so smallest is plotted last
    unique_uids = uid_totals["UID"]

    # Determine color scale
    if color_by_agg_option in numeric_agg_options:
        custom_colors = ["#0081a7", "#00afb9", "#fdfcdc", "#fed9b7", "#f07167"]
        color_map = create_continuous_cmap(custom_colors, n_colors=50)
        values = pd.to_numeric(plot_data[color_by_agg_option], errors="coerce").dropna()
        if not values.empty:
            min_val, max_val = values.min(), values.max()
            if max_val > min_val:
                color_indices = np.interp(
                    values, [min_val, max_val], [0, len(color_map) - 1]
                ).astype(int)
                color_map = {
                    uid: color_map[idx]
                    for uid, idx in zip(plot_data["UID"], color_indices)
                }
            else:
                color_map = {uid: color_map[0] for uid in plot_data["UID"].unique()}
        else:
            color_map = {uid: "#0081a7" for uid in plot_data["UID"].unique()}
    elif color_by_agg_option in categorical_agg_options:
        # Sort UIDs by color_by_agg_option for legend
        unique_uids_color = (
            plot_data[["UID", color_by_agg_option]]
            .drop_duplicates()
            .sort_values(color_by_agg_option)["UID"]
        )
        color_map = {
            uid: px.colors.qualitative.Dark24[i % len(px.colors.qualitative.Dark24)]
            for i, uid in enumerate(unique_uids_color)
        }
    else:
        color_map = {
            uid: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
            for i, uid in enumerate(plot_data["UID"].unique())
        }

    fig = go.Figure()

    # Iterate over UIDs sorted by total area (smallest last, in front)
    for val in unique_uids:
        mask = plot_data["UID"] == val
        fig.add_scatter(
            x=plot_data[mask][x_axis_select],
            y=plot_data[mask][y_axis_select],
            mode="lines",
            fill="tozeroy",
            name=str(val),
            line_color=color_map.get(val, "blue"),
            opacity=0.6,
        )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI, Arial, sans-serif", size=12, color="black"),
        xaxis=dict(
            type="date" if x_axis_select in ["Datetime", "YEAR_WEEK"] else None,
            title=dict(
                text=x_axis_select.replace("_", " ").title(),
                font=dict(color="black", size=14),
            ),
            tickfont=dict(color="black"),
            showgrid=True,
            gridcolor="lightgray",
            zeroline=False,
            showline=True,
            linecolor="black",
            ticks="outside",
            tickcolor="black",
            ticklen=5,
            tickformat="%Y-%U" if x_axis_select == "YEAR_WEEK" else "%Y-%m-%d",
        ),
        yaxis=dict(
            title=dict(
                text=y_axis_select.replace("_", " ").title(),
                font=dict(color="black", size=14),
            ),
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
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="lightgray",
            borderwidth=1,
            font=dict(color="black", size=11),
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
        ),
        margin=dict(l=50, r=150, t=80, b=50),
        title=dict(
            text=plot_title,
            font=dict(color="black", size=18, family="Segoe UI, Arial, sans-serif"),
            x=0.5,
            xanchor="center",
        ),
        hovermode="closest",
    )

    return fig


def plot_line_plot_columbia_dams(
    plot_data, plot_title, x_axis_select, y_axis_select, color_by_agg_option=None
):
    """
    Create a line plot for Columbia dams data with dynamic color scaling.
    """
    if not isinstance(plot_data, pd.DataFrame):
        raise ValueError("plot_data must be a pandas DataFrame")
    if x_axis_select not in plot_data.columns or y_axis_select not in plot_data.columns:
        raise ValueError("Selected axis columns must exist in the DataFrame")
    if "UID" not in plot_data.columns:
        raise ValueError("DataFrame must contain 'UID' column")

    # Handle YEAR_WEEK format if used
    if x_axis_select == "YEAR_WEEK":
        plot_data = plot_data.copy()
        plot_data[x_axis_select] = pd.to_datetime(
            plot_data[x_axis_select] + "-0", format="%Y-%U-%w", errors="coerce"
        )

    numeric_agg_options = ["DATE", "DOY", "WOY", "MONTH", "YEAR"]
    categorical_agg_options = ["SPECIES", "DAM", "LOCATION"]

    # Sort data by color_by_agg_option and x_axis_select if provided
    if color_by_agg_option is not None:
        plot_data = plot_data.sort_values([color_by_agg_option, x_axis_select])
    else:
        plot_data = plot_data.sort_values(x_axis_select)
    plot_data = plot_data.reset_index(drop=True)

    # Determine color scale
    if color_by_agg_option in numeric_agg_options:
        custom_colors = ["#0081a7", "#00afb9", "#fdfcdc", "#fed9b7", "#f07167"]
        color_map = create_continuous_cmap(custom_colors, n_colors=50)
        values = pd.to_numeric(plot_data[color_by_agg_option], errors="coerce").dropna()
        if not values.empty:
            min_val, max_val = values.min(), values.max()
            if max_val > min_val:
                color_indices = np.interp(
                    values, [min_val, max_val], [0, len(color_map) - 1]
                ).astype(int)
                color_map = {
                    uid: color_map[idx]
                    for uid, idx in zip(plot_data["UID"], color_indices)
                }
            else:
                color_map = {uid: color_map[0] for uid in plot_data["UID"].unique()}
        else:
            color_map = {uid: "#0081a7" for uid in plot_data["UID"].unique()}
    elif color_by_agg_option in categorical_agg_options:
        unique_uids = (
            plot_data[["UID", color_by_agg_option]]
            .drop_duplicates()
            .sort_values(color_by_agg_option)["UID"]
        )
        color_map = {
            uid: px.colors.qualitative.Dark24[i % len(px.colors.qualitative.Dark24)]
            for i, uid in enumerate(unique_uids)
        }
    else:
        color_map = {
            uid: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
            for i, uid in enumerate(plot_data["UID"].unique())
        }

    fig = go.Figure()

    unique_uids = (
        plot_data[["UID", color_by_agg_option]]
        .drop_duplicates()
        .sort_values(color_by_agg_option)["UID"]
        if color_by_agg_option
        else plot_data["UID"].unique()
    )
    for val in unique_uids:
        mask = plot_data["UID"] == val
        fig.add_scatter(
            x=plot_data[mask][x_axis_select],
            y=plot_data[mask][y_axis_select],
            mode="lines",
            line=dict(width=2),
            name=str(val),
            line_color=color_map.get(val, "blue"),
        )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI, Arial, sans-serif", size=12, color="black"),
        xaxis=dict(
            type="date" if x_axis_select in ["Datetime", "YEAR_WEEK"] else None,
            title=dict(
                text=x_axis_select.replace("_", " ").title(),
                font=dict(color="black", size=14),
            ),
            tickfont=dict(color="black"),
            showgrid=True,
            gridcolor="lightgray",
            zeroline=False,
            showline=True,
            linecolor="black",
            ticks="outside",
            tickcolor="black",
            ticklen=5,
            tickformat="%Y-%U" if x_axis_select == "YEAR_WEEK" else "%Y-%m-%d",
        ),
        yaxis=dict(
            title=dict(
                text=y_axis_select.replace("_", " ").title(),
                font=dict(color="black", size=14),
            ),
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
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="lightgray",
            borderwidth=1,
            font=dict(color="black", size=11),
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
        ),
        margin=dict(l=50, r=150, t=80, b=50),
        title=dict(
            text=plot_title,
            font=dict(color="black", size=18, family="Segoe UI, Arial, sans-serif"),
            x=0.5,
            xanchor="center",
        ),
        hovermode="closest",
    )

    return fig


def plot_bar_plot_columbia_dams(
    plot_data, plot_title, x_axis_select, y_axis_select, color_by_agg_option=None
):
    """
    Create a bar plot for Columbia dams data with dynamic color scaling.
    """
    if not isinstance(plot_data, pd.DataFrame):
        raise ValueError("plot_data must be a pandas DataFrame")
    if x_axis_select not in plot_data.columns or y_axis_select not in plot_data.columns:
        raise ValueError("Selected axis columns must exist in the DataFrame")
    if "UID" not in plot_data.columns:
        raise ValueError("DataFrame must contain 'UID' column'")

    # Handle YEAR_WEEK format if used
    if x_axis_select == "YEAR_WEEK":
        plot_data = plot_data.copy()
        plot_data[x_axis_select] = pd.to_datetime(
            plot_data[x_axis_select] + "-0", format="%Y-%U-%w", errors="coerce"
        )

    numeric_agg_options = ["DATE", "DOY", "WOY", "MONTH", "YEAR"]
    categorical_agg_options = ["SPECIES", "DAM", "LOCATION"]

    # Sort data by color_by_agg_option and x_axis_select if provided
    if color_by_agg_option is not None:
        plot_data = plot_data.sort_values([color_by_agg_option, x_axis_select])
    else:
        plot_data = plot_data.sort_values(x_axis_select)
    plot_data = plot_data.reset_index(drop=True)

    # Determine color scale
    if color_by_agg_option in numeric_agg_options:
        custom_colors = ["#0081a7", "#00afb9", "#fdfcdc", "#fed9b7", "#f07167"]
        color_map = create_continuous_cmap(custom_colors, n_colors=50)
        values = pd.to_numeric(plot_data[color_by_agg_option], errors="coerce").dropna()
        if not values.empty:
            min_val, max_val = values.min(), values.max()
            if max_val > min_val:
                color_indices = np.interp(
                    values, [min_val, max_val], [0, len(color_map) - 1]
                ).astype(int)
                color_map = {
                    uid: color_map[idx]
                    for uid, idx in zip(plot_data["UID"], color_indices)
                }
            else:
                color_map = {uid: color_map[0] for uid in plot_data["UID"].unique()}
        else:
            color_map = {uid: "#0081a7" for uid in plot_data["UID"].unique()}
    elif color_by_agg_option in categorical_agg_options:
        unique_uids = (
            plot_data[["UID", color_by_agg_option]]
            .drop_duplicates()
            .sort_values(color_by_agg_option)["UID"]
        )
        color_map = {
            uid: px.colors.qualitative.Dark24[i % len(px.colors.qualitative.Dark24)]
            for i, uid in enumerate(unique_uids)
        }
    else:
        color_map = {
            uid: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
            for i, uid in enumerate(plot_data["UID"].unique())
        }

    fig = go.Figure()

    unique_uids = (
        plot_data[["UID", color_by_agg_option]]
        .drop_duplicates()
        .sort_values(color_by_agg_option)["UID"]
        if color_by_agg_option
        else plot_data["UID"].unique()
    )
    for val in unique_uids:
        mask = plot_data["UID"] == val
        fig.add_bar(
            x=plot_data[mask][x_axis_select],
            y=plot_data[mask][y_axis_select],
            name=str(val),
            marker_color=color_map.get(val, "blue"),
            opacity=0.8,
        )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI, Arial, sans-serif", size=12, color="black"),
        xaxis=dict(
            type="date" if x_axis_select in ["Datetime", "YEAR_WEEK"] else None,
            title=dict(
                text=x_axis_select.replace("_", " ").title(),
                font=dict(color="black", size=14),
            ),
            tickfont=dict(color="black"),
            showgrid=True,
            gridcolor="lightgray",
            zeroline=False,
            showline=True,
            linecolor="black",
            ticks="outside",
            tickcolor="black",
            ticklen=5,
            tickformat="%Y-%U" if x_axis_select == "YEAR_WEEK" else "%Y-%m-%d",
        ),
        yaxis=dict(
            title=dict(
                text=y_axis_select.replace("_", " ").title(),
                font=dict(color="black", size=14),
            ),
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
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="lightgray",
            borderwidth=1,
            font=dict(color="black", size=11),
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
        ),
        margin=dict(l=50, r=150, t=80, b=50),
        title=dict(
            text=plot_title,
            font=dict(color="black", size=18, family="Segoe UI, Arial, sans-serif"),
            x=0.5,
            xanchor="center",
        ),
        barmode="group",
        hovermode="closest",
    )

    return fig


####################### - plot_area_plot_orca_sightings


def plot_area_plot_orca_sightings(
    plot_data, plot_title, x_axis_select, y_axis_select, color_by_agg_option=None
):
    """
    Create an area plot for Columbia dams data with dynamic color scaling, sorting areas by total size (smallest in front).

    Args:
        plot_data (pd.DataFrame): Input DataFrame with columns including UID, x_axis_select, y_axis_select
        plot_title (str): Title of the plot
        x_axis_select (str): Column name for x-axis
        y_axis_select (str): Column name for y-axis
        color_by_agg_option (str, optional): Aggregation option to color by (numeric or categorical)
    """
    if not isinstance(plot_data, pd.DataFrame):
        raise ValueError("plot_data must be a pandas DataFrame")
    if x_axis_select not in plot_data.columns or y_axis_select not in plot_data.columns:
        raise ValueError("Selected axis columns must exist in the DataFrame")
    if "UID" not in plot_data.columns:
        raise ValueError("DataFrame must contain 'UID' column")

    # Handle YEAR_WEEK format if used
    if x_axis_select == "YEAR_WEEK":
        plot_data = plot_data.copy()
        plot_data[x_axis_select] = pd.to_datetime(
            plot_data[x_axis_select] + "-0", format="%Y-%U-%w", errors="coerce"
        )

    numeric_agg_options = ["DATE", "DOY", "WOY", "MONTH", "YEAR"]
    categorical_agg_options = ["SPECIES", "DAM", "LOCATION"]

    # Sort data by color_by_agg_option and x_axis_select if provided
    if color_by_agg_option is not None:
        plot_data = plot_data.sort_values([color_by_agg_option, x_axis_select])
    else:
        plot_data = plot_data.sort_values(x_axis_select)
    plot_data = plot_data.reset_index(drop=True)

    # Calculate total y_axis_select values for each UID to sort areas (smallest in front)
    uid_totals = plot_data.groupby("UID")[y_axis_select].sum().reset_index()
    uid_totals = uid_totals.sort_values(
        y_axis_select, ascending=False
    )  # Descending so smallest is plotted last
    unique_uids = uid_totals["UID"]

    # Determine color scale
    if color_by_agg_option in numeric_agg_options:
        custom_colors = ["#0081a7", "#00afb9", "#fdfcdc", "#fed9b7", "#f07167"]
        color_map = create_continuous_cmap(custom_colors, n_colors=50)
        values = pd.to_numeric(plot_data[color_by_agg_option], errors="coerce").dropna()
        if not values.empty:
            min_val, max_val = values.min(), values.max()
            if max_val > min_val:
                color_indices = np.interp(
                    values, [min_val, max_val], [0, len(color_map) - 1]
                ).astype(int)
                color_map = {
                    uid: color_map[idx]
                    for uid, idx in zip(plot_data["UID"], color_indices)
                }
            else:
                color_map = {uid: color_map[0] for uid in plot_data["UID"].unique()}
        else:
            color_map = {uid: "#0081a7" for uid in plot_data["UID"].unique()}
    elif color_by_agg_option in categorical_agg_options:
        # Sort UIDs by color_by_agg_option for legend
        unique_uids_color = (
            plot_data[["UID", color_by_agg_option]]
            .drop_duplicates()
            .sort_values(color_by_agg_option)["UID"]
        )
        color_map = {
            uid: px.colors.qualitative.Dark24[i % len(px.colors.qualitative.Dark24)]
            for i, uid in enumerate(unique_uids_color)
        }
    else:
        color_map = {
            uid: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
            for i, uid in enumerate(plot_data["UID"].unique())
        }

    fig = go.Figure()

    # Iterate over UIDs sorted by total area (smallest last, in front)
    for val in unique_uids:
        mask = plot_data["UID"] == val
        fig.add_scatter(
            x=plot_data[mask][x_axis_select],
            y=plot_data[mask][y_axis_select],
            mode="lines",
            fill="tozeroy",
            name=str(val),
            line_color=color_map.get(val, "blue"),
            opacity=0.6,
        )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI, Arial, sans-serif", size=12, color="black"),
        xaxis=dict(
            type="date" if x_axis_select in ["Datetime", "YEAR_WEEK"] else None,
            title=dict(
                text=x_axis_select.replace("_", " ").title(),
                font=dict(color="black", size=14),
            ),
            tickfont=dict(color="black"),
            showgrid=True,
            gridcolor="lightgray",
            zeroline=False,
            showline=True,
            linecolor="black",
            ticks="outside",
            tickcolor="black",
            ticklen=5,
            tickformat="%Y-%U" if x_axis_select == "YEAR_WEEK" else "%Y-%m-%d",
        ),
        yaxis=dict(
            title=dict(
                text=y_axis_select.replace("_", " ").title(),
                font=dict(color="black", size=14),
            ),
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
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="lightgray",
            borderwidth=1,
            font=dict(color="black", size=11),
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
        ),
        margin=dict(l=50, r=150, t=80, b=50),
        title=dict(
            text=plot_title,
            font=dict(color="black", size=18, family="Segoe UI, Arial, sans-serif"),
            x=0.5,
            xanchor="center",
        ),
        hovermode="closest",
    )

    return fig


def plot_line_plot_orca_sightings(
    plot_data, plot_title, x_axis_select, y_axis_select, color_by_agg_option=None
):
    """
    Create a line plot for Columbia dams data with dynamic color scaling.
    """
    if not isinstance(plot_data, pd.DataFrame):
        raise ValueError("plot_data must be a pandas DataFrame")
    if x_axis_select not in plot_data.columns or y_axis_select not in plot_data.columns:
        raise ValueError("Selected axis columns must exist in the DataFrame")
    if "UID" not in plot_data.columns:
        raise ValueError("DataFrame must contain 'UID' column")

    # Handle YEAR_WEEK format if used
    if x_axis_select == "YEAR_WEEK":
        plot_data = plot_data.copy()
        plot_data[x_axis_select] = pd.to_datetime(
            plot_data[x_axis_select] + "-0", format="%Y-%U-%w", errors="coerce"
        )

    numeric_agg_options = ["DATE", "DOY", "WOY", "MONTH", "YEAR"]
    categorical_agg_options = ["SPECIES", "DAM", "LOCATION"]

    # Sort data by color_by_agg_option and x_axis_select if provided
    if color_by_agg_option is not None:
        plot_data = plot_data.sort_values([color_by_agg_option, x_axis_select])
    else:
        plot_data = plot_data.sort_values(x_axis_select)
    plot_data = plot_data.reset_index(drop=True)

    # Determine color scale
    if color_by_agg_option in numeric_agg_options:
        custom_colors = ["#0081a7", "#00afb9", "#fdfcdc", "#fed9b7", "#f07167"]
        color_map = create_continuous_cmap(custom_colors, n_colors=50)
        values = pd.to_numeric(plot_data[color_by_agg_option], errors="coerce").dropna()
        if not values.empty:
            min_val, max_val = values.min(), values.max()
            if max_val > min_val:
                color_indices = np.interp(
                    values, [min_val, max_val], [0, len(color_map) - 1]
                ).astype(int)
                color_map = {
                    uid: color_map[idx]
                    for uid, idx in zip(plot_data["UID"], color_indices)
                }
            else:
                color_map = {uid: color_map[0] for uid in plot_data["UID"].unique()}
        else:
            color_map = {uid: "#0081a7" for uid in plot_data["UID"].unique()}
    elif color_by_agg_option in categorical_agg_options:
        unique_uids = (
            plot_data[["UID", color_by_agg_option]]
            .drop_duplicates()
            .sort_values(color_by_agg_option)["UID"]
        )
        color_map = {
            uid: px.colors.qualitative.Dark24[i % len(px.colors.qualitative.Dark24)]
            for i, uid in enumerate(unique_uids)
        }
    else:
        color_map = {
            uid: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
            for i, uid in enumerate(plot_data["UID"].unique())
        }

    fig = go.Figure()

    unique_uids = (
        plot_data[["UID", color_by_agg_option]]
        .drop_duplicates()
        .sort_values(color_by_agg_option)["UID"]
        if color_by_agg_option
        else plot_data["UID"].unique()
    )
    for val in unique_uids:
        mask = plot_data["UID"] == val
        fig.add_scatter(
            x=plot_data[mask][x_axis_select],
            y=plot_data[mask][y_axis_select],
            mode="markers",
            line=dict(width=2),
            name=str(val),
            line_color=color_map.get(val, "blue"),
        )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI, Arial, sans-serif", size=12, color="black"),
        xaxis=dict(
            type="date" if x_axis_select in ["Datetime", "YEAR_WEEK"] else None,
            title=dict(
                text=x_axis_select.replace("_", " ").title(),
                font=dict(color="black", size=14),
            ),
            tickfont=dict(color="black"),
            showgrid=True,
            gridcolor="lightgray",
            zeroline=False,
            showline=True,
            linecolor="black",
            ticks="outside",
            tickcolor="black",
            ticklen=5,
            tickformat="%Y-%U" if x_axis_select == "YEAR_WEEK" else "%Y-%m-%d",
        ),
        yaxis=dict(
            title=dict(
                text=y_axis_select.replace("_", " ").title(),
                font=dict(color="black", size=14),
            ),
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
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="lightgray",
            borderwidth=1,
            font=dict(color="black", size=11),
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
        ),
        margin=dict(l=50, r=150, t=80, b=50),
        title=dict(
            text=plot_title,
            font=dict(color="black", size=18, family="Segoe UI, Arial, sans-serif"),
            x=0.5,
            xanchor="center",
        ),
        hovermode="closest",
    )

    return fig


def plot_bar_plot_orca_sightings(
    plot_data, plot_title, x_axis_select, y_axis_select, color_by_agg_option=None
):
    """
    Create a bar plot for Columbia dams data with dynamic color scaling.
    """
    if not isinstance(plot_data, pd.DataFrame):
        raise ValueError("plot_data must be a pandas DataFrame")
    if x_axis_select not in plot_data.columns or y_axis_select not in plot_data.columns:
        raise ValueError("Selected axis columns must exist in the DataFrame")
    if "UID" not in plot_data.columns:
        raise ValueError("DataFrame must contain 'UID' column'")

    # Handle YEAR_WEEK format if used
    if x_axis_select == "YEAR_WEEK":
        plot_data = plot_data.copy()
        plot_data[x_axis_select] = pd.to_datetime(
            plot_data[x_axis_select] + "-0", format="%Y-%U-%w", errors="coerce"
        )

    numeric_agg_options = ["DATE", "DOY", "WOY", "MONTH", "YEAR"]
    categorical_agg_options = ["SPECIES", "DAM", "LOCATION"]

    # Sort data by color_by_agg_option and x_axis_select if provided
    if color_by_agg_option is not None:
        plot_data = plot_data.sort_values([color_by_agg_option, x_axis_select])
    else:
        plot_data = plot_data.sort_values(x_axis_select)
    plot_data = plot_data.reset_index(drop=True)

    # Determine color scale
    if color_by_agg_option in numeric_agg_options:
        custom_colors = ["#0081a7", "#00afb9", "#fdfcdc", "#fed9b7", "#f07167"]
        color_map = create_continuous_cmap(custom_colors, n_colors=50)
        values = pd.to_numeric(plot_data[color_by_agg_option], errors="coerce").dropna()
        if not values.empty:
            min_val, max_val = values.min(), values.max()
            if max_val > min_val:
                color_indices = np.interp(
                    values, [min_val, max_val], [0, len(color_map) - 1]
                ).astype(int)
                color_map = {
                    uid: color_map[idx]
                    for uid, idx in zip(plot_data["UID"], color_indices)
                }
            else:
                color_map = {uid: color_map[0] for uid in plot_data["UID"].unique()}
        else:
            color_map = {uid: "#0081a7" for uid in plot_data["UID"].unique()}
    elif color_by_agg_option in categorical_agg_options:
        unique_uids = (
            plot_data[["UID", color_by_agg_option]]
            .drop_duplicates()
            .sort_values(color_by_agg_option)["UID"]
        )
        color_map = {
            uid: px.colors.qualitative.Dark24[i % len(px.colors.qualitative.Dark24)]
            for i, uid in enumerate(unique_uids)
        }
    else:
        color_map = {
            uid: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
            for i, uid in enumerate(plot_data["UID"].unique())
        }

    fig = go.Figure()

    unique_uids = (
        plot_data[["UID", color_by_agg_option]]
        .drop_duplicates()
        .sort_values(color_by_agg_option)["UID"]
        if color_by_agg_option
        else plot_data["UID"].unique()
    )
    for val in unique_uids:
        mask = plot_data["UID"] == val
        fig.add_bar(
            x=plot_data[mask][x_axis_select],
            y=plot_data[mask][y_axis_select],
            name=str(val),
            marker_color=color_map.get(val, "blue"),
            opacity=0.8,
        )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI, Arial, sans-serif", size=12, color="black"),
        xaxis=dict(
            type="date" if x_axis_select in ["Datetime", "YEAR_WEEK"] else None,
            title=dict(
                text=x_axis_select.replace("_", " ").title(),
                font=dict(color="black", size=14),
            ),
            tickfont=dict(color="black"),
            showgrid=True,
            gridcolor="lightgray",
            zeroline=False,
            showline=True,
            linecolor="black",
            ticks="outside",
            tickcolor="black",
            ticklen=5,
            tickformat="%Y-%U" if x_axis_select == "YEAR_WEEK" else "%Y-%m-%d",
        ),
        yaxis=dict(
            title=dict(
                text=y_axis_select.replace("_", " ").title(),
                font=dict(color="black", size=14),
            ),
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
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="lightgray",
            borderwidth=1,
            font=dict(color="black", size=11),
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
        ),
        margin=dict(l=50, r=150, t=80, b=50),
        title=dict(
            text=plot_title,
            font=dict(color="black", size=18, family="Segoe UI, Arial, sans-serif"),
            x=0.5,
            xanchor="center",
        ),
        barmode="group",
        hovermode="closest",
    )

    return fig
