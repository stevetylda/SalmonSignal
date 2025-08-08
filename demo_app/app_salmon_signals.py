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
    "Analysis - Rivers": [
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
        st.Page(
            f"../demo_app/pages/4_Sacramento_River.py",
            title="Sacramento River",
            icon=":material/water:",
        ),
    ],
    "Analysis - Open Ocean": [
        st.Page(
            f"../demo_app/pages/5_Coastal_British_Columbia.py",
            title="Coastal - British Columbia",
            icon=":material/tsunami:",
        ),
        st.Page(
            f"../demo_app/pages/6_Coastal_California.py",
            title="Coastal - California",
            icon=":material/tsunami:",
        ),
        st.Page(
            f"../demo_app/pages/7_Coastal_Oregon.py",
            title="Coastal - Oregon",
            icon=":material/tsunami:",
        ),
        st.Page(
            f"../demo_app/pages/8_Coastal_Washington.py",
            title="Coastal - Washington",
            icon=":material/tsunami:",
        ),
    ],
    # "Learn More": [
    #     st.Page(
    #         f"../demo_app/pages/9_Learn_More.py",
    #         title="Learn More",
    #         icon=":material/info:",
    #     )
    # ],
    # "About": [
    #     st.Page(
    #         f"../demo_app/pages/10_About.py",
    #         title="About",
    #         icon=":material/info:",
    #     )
    # ],
}

# Configure navigation
# pages = [page0, page1, page2]
app = st.navigation(pages=pages, position="top")

# Run App
app.run()

###################################################################################
