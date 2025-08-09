import streamlit as st
import base64
import os


def get_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# Top Image Banner
def load_top_image_banner(top_image_path):
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

    if os.path.exists(f"./demo_app/assets/{top_image_path}"):
        st.image(f"./demo_app/assets/{top_image_path}")
    elif os.path.exists(f"./../demo_app/assets/{top_image_path}"):
        st.image(f"./../demo_app/assets/{top_image_path}")
