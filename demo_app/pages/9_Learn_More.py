import streamlit as st

from src.auth import check_password_user

if not check_password_user():
    st.stop()

st.set_page_config(page_title="Learn More", layout="wide")

st.title("Learn More")
st.write("Learn More About Salmon Prey Predator Interaction")
