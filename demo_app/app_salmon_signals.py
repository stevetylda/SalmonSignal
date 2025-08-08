"""Salmon Signals Demo Application"""

import streamlit as st

# ---- Load and convert background image to base64 ----
st.set_page_config(
    page_title="First app",
    page_icon=":material/home:",
    initial_sidebar_state="collapsed",
    layout="wide",
)

###################################################################################

pages = {
    "Overview": [
        st.Page(
            f"../demo_app/pages/0_Overview.py",
            title="Overview",
            icon=":material/home:",
        )
    ],
    "Analysis": [
        st.Page(
            f"../demo_app/pages/1_Ballard_Locks.py",
            title="Ballard Locks",
            icon=":material/water:",
        ),
        st.Page(
            f"../demo_app/pages/2_Columbia_River.py",
            title="Columbia River",
            icon=":material/water:",
        ),
        st.Page(
            f"../demo_app/pages/3_Fraser_River.py",
            title="Fraser River",
            icon=":material/water:",
        ),
    ],
    "About": [
        st.Page(
            f"../demo_app/pages/4_About.py",
            title="About",
            icon=":material/info:",
        )
    ],
}

# Configure navigation
# pages = [page0, page1, page2]
app = st.navigation(pages=pages, position="top")

# Run App
app.run()

###################################################################################
