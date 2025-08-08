import streamlit as st
from src.utils import get_base64

st.set_page_config(page_title="SRKW Salmon Signals - Overview", layout="wide")

# ---- Load and convert background image to base64 ----

img_base64 = get_base64("assets/lachlan_orca_image.jpg")  # Your local image

# ---- CSS Styling ----
st.markdown(
    f"""
<style>
/* Background image setup */
#bg-img {{
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    opacity: 0.5;
    z-index: 0;
    pointer-events: none;
}}

/* Main content box styling */
.st-key-main_box {{
    background-color: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(8px);
    border-radius: 24px;
    padding: 3rem;
    margin: 2rem auto;
    max-width: 96%;
    color: white;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    z-index: 10;
}}

.footer-note {{
    text-align: center;
    font-size: 0.9rem;
    color: #cccccc;
    margin-top: 1rem;
    margin-bottom: 3rem;
    font-style: italic;
}}

/* Demo banner */
#demo-banner {{
    background-color: #f5f1a4;
    padding: 12px;
    border: 1.5px solid #d4c85d;
    border-radius: 16px;
    font-size: 16px;
    text-align: center;
    font-weight: 700;
    color: #1a2238;
    margin-bottom: 30px;
}}

/* Shared card style */
.card {{
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 2px solid;
    border-image-slice: 1;
    border-width: 2px;
    border-image-source: linear-gradient(120deg, #c1c1c1, #e0e0e0, #c1c1c1);
    padding: 24px 20px;
    margin-bottom: 16px;
    color: #e9e9e9;
    font-size: 15px;
    line-height: 1.4;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    transition: all 0.4s ease;
}}
.card:hover {{
    box-shadow: 0 4px 25px rgba(255, 255, 255, 0.3);
    transform: translateY(-3px);
    border-image-source: linear-gradient(300deg, #f0f0f0, #ffffff, #f0f0f0);
    color: #ffffff;
    cursor: pointer;
}}
.card h4 {{
    margin-top: 0;
    margin-bottom: 12px;
    color: #f0f0f0; 
    font-weight: 600; 
}}
.card h3 {{
    margin-top: 0;
    margin-bottom: 14px;
    color: #f0f0f0; 
    font-weight: 600; 
}}
.card h2 {{
    margin-top: 0;
    margin-bottom: 16px;
    color: #f0f0f0; 
    font-weight: 600; 
}}
.card p {{
    margin-bottom: 0;
    color: #c0c0c0;
}}
.nav-button {{
        min-height: 160px;
        max-width: 400px;
        width: 100%;
        margin: 10px auto; /* center horizontally */
        padding: 24px 20px;
        border-radius: 24px;
        border: 2.5px solid #CBD4C2;
        background: rgba(20, 30, 60, 0.3);
        color: #d0e6ff;
        font-weight: 600;
        font-size: 17px;
        cursor: pointer;
        transition: all 0.35s ease;
        text-align: center;
        box-shadow: none;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-decoration: none;
    }}
    .nav-button:hover {{
        border-image-source: linear-gradient(120deg, #c1c1c1, #e0e0e0, #c1c1c1);
        border-image-slice: 1;
        background: rgba(255, 255, 255, 0.15);
        color: #ffffff;
        box-shadow: 0 5px 28px rgba(255, 255, 255, 0.4);
        transform: translateY(-3px);
    }}
    .nav-button h4 {{
        margin: 0 0 10px 0;
        color: inherit;
    }}
    .nav-button p {{
        margin: 0;
        color: #aac9ff;
        font-size: 14px;
    }}
</style>

<!-- Background image element -->
<div id="bg-img"></div>
""",
    unsafe_allow_html=True,
)

# ---- Main Page Content in Container ----
with st.container(key="main_box"):
    st.markdown(
        '<div id="demo-banner">DEMO APPLICATION – Data and results are for demonstration purposes only.</div>',
        unsafe_allow_html=True,
    )

    st.title(
        "Salmon Signals - Prey Analysis for the Southern Resident Killer Whale (SRKW)"
    )
    st.subheader(
        "Exploring Salmon Counts, Pinniped Pressure, and Environmental Covariates"
    )

    st.markdown(
        """
    This application demonstrates how salmon migration patterns, pinniped interactions, and environmental conditions can be visualized to better understand prey availability for **Southern Resident Killer Whales (SRKWs)**.

    **Note:** This is a prototype interface using a mix of sample and historical data. It is not intended for operational or policy decisions.
    """
    )

    st.markdown("---")
    st.header("Key Indicators Overview")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
        <div class="card">
            <h4>Salmon Counts</h4>
            <p>Tracking salmon passage and migration timing.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="card">
            <h4>Pinniped Pressure</h4>
            <p>Understanding seal and sea lion presence that may intercept prey.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="card">
            <h4>Environmental Covariates</h4>
            <p>Exploring factors like temperature, flow, and more.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.header("About this Demo")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(
            """
        <div class="card">
            <h4>Simplified Data</h4>
            <p>Aggregated or sample datasets are used for demonstration purposes.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col5:
        st.markdown(
            """
        <div class="card">
            <h4>Partial Coverage</h4>
            <p>Only a subset of data sources are integrated at this stage.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col6:
        st.markdown(
            """
        <div class="card">
            <h4>Static Updates</h4>
            <p>No real-time feeds; visualizations reflect historical or sample data.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.header("Available Pages")

    col7, col8 = st.columns(2)

    with col7:
        st.markdown(
            """
            <a href="Columbia_River" class="nav-button" style="text-decoration:none;">
                <h4>Columbia River</h4>
                <p>Explore migration timing, passage counts, and associated environmental factors.</p>
            </a>
            """,
            unsafe_allow_html=True,
        )

    with col8:
        st.markdown(
            """
            <a href="About" class="nav-button" style="text-decoration:none;">
                <h4>About</h4>
                <p>Learn more about the methodology and data sources.</p>
            </a>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <div class="footer-note">
        For support or questions, reach out to <a href="mailto:<demo-email>@gmail.com" style="color:#a8dadc;">support@example.com</a>.
        Thank you for exploring the SRKW Salmon Signals demo.
    </div>
    """,
    unsafe_allow_html=True,
)
