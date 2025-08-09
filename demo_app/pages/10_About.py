import streamlit as st

from src.auth import check_password_user

if not check_password_user():
    st.stop()

st.set_page_config(page_title="About", layout="wide")

st.title("About")
st.write("About the SalmonSignal App.")
