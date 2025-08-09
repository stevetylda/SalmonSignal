# ------------------------------------------------------- #
#                         MODULES                         #

# Standard Modules
import os

# Third-Party Modules
import folium
import streamlit as st
import geopandas as gpd
from shapely.geometry import mapping

#                                                         #
# ------------------------------------------------------- #

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
