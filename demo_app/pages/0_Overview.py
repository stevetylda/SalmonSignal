import streamlit as st
from src.utils import get_base64

from src.auth import check_password_user

if not check_password_user():
    st.stop()

st.set_page_config(page_title="SRKW Salmon Signals - Overview", layout="wide")

# ---- Load and convert background image to base64 ----
import os

base_image_path_1 = f"../demo_app/assets/lachlan_orca_image.jpg"
base_image_path_2 = f"./demo_app/assets/lachlan_orca_image.jpg"

if os.path.exists(base_image_path_1):
    img_path = base_image_path_1
elif os.path.exists(base_image_path_2):
    img_path = base_image_path_2
else:
    print("Image path does not exist")
    print(os.listdir())

# Open Base Image
img_base64 = get_base64(img_path)  # Your local image

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
    /* Gradient Glow Ring on Nav Buttons (both .nav-button and .nav-button-2) */
    .nav-button, .nav-button-2 {{
        position: relative;
        overflow: hidden;
        border-radius: 24px;
        padding: 24px 20px;
        transition: all 0.35s ease;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-decoration: none;
        max-width: 400px;
        margin: 10px auto;
        font-weight: 600;
        font-size: 17px;
        box-shadow: none;
        color: #d0e6ff; /* fallback color */
    }}

    /* Glow ring effect */
    .nav-button::before, .nav-button-2::before {{
        content: "";
        position: absolute;
        inset: -4px;
        border-radius: 30px;
        background: linear-gradient(120deg, #89f7fe, #66a6ff, #89f7fe);
        filter: blur(12px);
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: -1;
    }}

    /* Show glow ring on hover for nav-button */
    .nav-button:hover::before {{
        opacity: 0.5;
    }}

    /* Show glow ring on hover for nav-button-2 */
    .nav-button-2:hover::before {{
        opacity: 0.5;
    }}

    /* Specific styling for nav-button */
    .nav-button {{
        background: rgba(20, 30, 60, 0.3);
        border: 2.5px solid #CBD4C2;
        color: #d0e6ff;
    }}

    .nav-button:hover {{
        background: rgba(255, 255, 255, 0.15);
        color: #ffffff;
        box-shadow: 0 5px 28px rgba(255, 255, 255, 0.4);
        transform: translateY(-3px);
        border-image-source: linear-gradient(120deg, #c1c1c1, #e0e0e0, #c1c1c1);
        border-image-slice: 1;
    }}

    /* Specific styling for nav-button-2 */
    .nav-button-2 {{
        background: rgba(255, 255, 255, 0.04);
        border: 2.5px dashed #999999;
        color: #cccccc;
        cursor: default;
        opacity: 0.7;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        transition: none;
    }}

    .nav-button-2:hover {{
        /* Lets keep hover subtle but still show glow */
        opacity: 1;
        cursor: pointer;
        box-shadow: 0 5px 28px rgba(255, 255, 255, 0.4);
        transform: translateY(-3px);
    }}

    /* Headings and paragraph inside nav-buttons */
    .nav-button h4, .nav-button-2 h4 {{
        margin: 0 0 10px 0;
        color: inherit;
        font-weight: 700;
        font-size: 20px;
    }}
    .nav-button p, .nav-button-2 p {{
        margin: 0;
        color: #aac9ff;
        font-size: 14px;
    }}

    /* Mini status badge */
    .status-badge {{
        position: absolute;
        top: 12px;
        right: 16px;
        background-color: #42a5f5;
        color: white;
        font-size: 11px;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        letter-spacing: 0.5px;
        box-shadow: 0 0 8px rgba(66, 165, 245, 0.4);
        z-index: 1;
        user-select: none;
    }}

    /* Fade-in-up animation */
    @keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(24px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
    .nav-button, .nav-button-2 {{
        animation: fadeInUp 0.6s ease both;
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
    st.header("Select a Topic to Learn More")

    # First Row of Links
    col7, col8, col9 = st.columns(3)

    with col7:
        st.markdown(
            """
            <a href="Ballard_Locks" class="nav-button-2" style="text-decoration:none;">
                <h4>Ballard Locks</h4>
                <p>Coming Soon!</p>
            </a>
            """,
            unsafe_allow_html=True,
        )

    with col8:
        st.markdown(
            """
            <a href="/Columbia_River" class="nav-button" style="text-decoration:none;">
                <h4>Columbia River</h4>
                <p>Explore migration timing, passage counts, and associated environmental factors.</p>
            </a>
            """,
            unsafe_allow_html=True,
        )

    with col9:
        st.markdown(
            """
            <a href="Fraser_River" class="nav-button-2" style="text-decoration:none;">
                <h4>Fraser River</h4>
                <p>Coming Soon!</p>
            </a>
            """,
            unsafe_allow_html=True,
        )

    # Second Row of Links
    col10, col11, col12 = st.columns(3)

    with col10:
        st.markdown(
            """
            <a href="Sacramento_River" class="nav-button-2" style="text-decoration:none;">
                <h4>Sacramento River</h4>
                <p>Coming Soon!</p>
            </a>
            """,
            unsafe_allow_html=True,
        )

    with col11:
        st.markdown(
            """
            <a href="British_Columbia_Coast" class="nav-button-2" style="text-decoration:none;">
                <h4>Coastal British Columbia</h4>
                <p>Coming Soon!</p>
            </a>
            """,
            unsafe_allow_html=True,
        )

    with col12:
        st.markdown(
            """
            <a href="California_Coast" class="nav-button-2" style="text-decoration:none;">
                <h4>Coastal California</h4>
                <p>Coming Soon!</p>
            </a>
            """,
            unsafe_allow_html=True,
        )

    # Third Row of Links
    col13, col14, col15 = st.columns(3)

    with col13:
        st.markdown(
            """
            <a href="Oregon_Coast" class="nav-button-2" style="text-decoration:none;">
                <h4>Coastal Oregon</h4>
                <p>Coming Soon!</p>
            </a>
            """,
            unsafe_allow_html=True,
        )

    with col14:
        st.markdown(
            """
            <a href="Washington_Coast" class="nav-button-2" style="text-decoration:none;">
                <h4>Coastal Washington</h4>
                <p>Coming Soon!</p>
            </a>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # with col10:
    #     st.markdown(
    #         """
    #         <a href="About" class="nav-button" style="text-decoration:none;">
    #             <h4>About</h4>
    #             <p>Learn more about the methodology and data sources.</p>
    #         </a>
    #         """,
    #         unsafe_allow_html=True,
    #     )

st.markdown(
    """
    <div class="footer-note">
        For support or questions, reach out to <a href="mailto:<demo-email>@gmail.com" style="color:#a8dadc;">support@example.com</a>.
        Thank you for exploring the SRKW Salmon Signals demo.
    </div>
    """,
    unsafe_allow_html=True,
)
