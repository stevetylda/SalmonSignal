# ----------------------------------------- #
#                  MODULES                  #

# Standard Modules
import os
import warnings

# Third-Party Modules
import geopandas as gpd
import h3
import numpy as np
import pandas as pd
import plotly.express as px
from shapely.geometry import box, Point, Polygon

#                                           #
# ----------------------------------------- #

# ----------------------------------------- #
#                 FUNCTIONS                 #


# Data Opener for Sightings Data
def open_sightings(path):
    if os.path.exists(path):
        if ".csv" in path:
            sightings = pd.read_csv(path)
            return sightings
        elif ".parquet" in path:
            sightings = pd.read_parquet(path)
            return sightings
    #     else:
    #         raise "WARNING: Unsupported file type - supported types include parquet and csv"
    else:
        print("WARNING: Path does not exist.")


# Quick Preprocess on Read of Sightings Data
def quick_preprocess(data):
    # Preprocess Sightings - Remove Spurious Data
    data["LONGITUDE"] = np.where(
        data["LONGITUDE"] > 0, data["LONGITUDE"] * -1, data["LONGITUDE"]
    )
    data = data[(data["LONGITUDE"] < -115) & (data["LONGITUDE"] > -160)]

    return data


# H3 Grid to Polygon
def h3_to_polygon(h3_index):
    boundary = h3.cell_to_boundary(h3_index)
    boundary_lonlat = [(lon, lat) for lat, lon in boundary]
    return Polygon(boundary_lonlat)


# Load Data
def load_sightings_data(SIGHTINGS_PATH, POD_TYPE, H3_RESOLUTION, start_date, end_date):
    sightings = open_sightings(path=SIGHTINGS_PATH)
    sightings = quick_preprocess(sightings)
    sightings["DATE"] = pd.to_datetime(sightings["DATE"])

    # Filter to Pod Type
    sightings = sightings[sightings["POD_TYPE"] == POD_TYPE].copy()

    # Expand by COUNT
    sightings_expanded = sightings.loc[
        sightings.index.repeat(sightings["COUNT"])
    ].reset_index(drop=True)

    # Assign H3 cell (parallelized with swifter)
    sightings_expanded["H3_CELL"] = sightings_expanded.apply(
        lambda x: h3.latlng_to_cell(x["LATITUDE"], x["LONGITUDE"], H3_RESOLUTION),
        axis=1,
    )

    # Generate binary target
    sightings_expanded["presence"] = 1

    # Generate absence rows (only for H3 cells that have ever had a sighting)
    h3_cells = sightings_expanded["H3_CELL"].unique()

    if start_date is None:
        start_date = sightings_expanded["DATE"].min()
    if end_date is None:
        end_date = sightings_expanded["DATE"].max()

    all_dates = pd.date_range(start=start_date, end=end_date, freq="D")
    all_h3_dates = pd.MultiIndex.from_product(
        [h3_cells, all_dates], names=["H3_CELL", "DATE"]
    )
    absence_df = pd.DataFrame(index=all_h3_dates).reset_index()

    # Merge with sightings to mark presence
    df_model = absence_df.merge(
        sightings_expanded[["H3_CELL", "DATE", "presence"]],
        on=["H3_CELL", "DATE"],
        how="left",
    )

    # Fill NaN with 0 for absence
    df_model["presence"] = df_model["presence"].fillna(0)

    # Only keep unique rows per H3_CELL/DATE for merge
    temporal_lookup = sightings_expanded[["H3_CELL", "DATE"]].drop_duplicates(
        subset=["H3_CELL", "DATE"]
    )
    df_model = df_model.merge(temporal_lookup, on=["H3_CELL", "DATE"], how="left")

    return df_model


# Preprocess Data
def add_features_sightings_data(df_model):
    # Add Temporal Features
    df_model["DOY"] = df_model["DATE"].dt.day_of_year
    df_model["DOW"] = df_model["DATE"].dt.day_of_week
    df_model["WOY"] = df_model["DATE"].dt.isocalendar().week
    df_model["MONTH"] = df_model["DATE"].dt.month
    df_model["YEAR"] = df_model["DATE"].dt.year

    df_model["MONTH_SIN"] = np.sin(2 * np.pi * df_model["MONTH"] / 12)
    df_model["MONTH_COS"] = np.cos(2 * np.pi * df_model["MONTH"] / 12)

    df_model["DOY_SIN"] = np.sin(2 * np.pi * df_model["MONTH"] / 12)
    df_model["DOY_COS"] = np.cos(2 * np.pi * df_model["MONTH"] / 12)

    df_model["WOY_SIN"] = np.sin(2 * np.pi * df_model["WOY"] / 52)
    df_model["WOY_COS"] = np.cos(2 * np.pi * df_model["WOY"] / 52)

    df_model = df_model.reset_index(drop=True)

    return df_model


#                                           #
# ----------------------------------------- #
