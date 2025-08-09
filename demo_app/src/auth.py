import streamlit as st

# --- Define your login credentials ---
GENERAL_USERNAME = "orcasalmon_admin"
GENERAL_PASSWORD = "salmon4srkw"


def check_password_user():
    """Returns True if the user had the correct password."""
    if "user_authenticated" not in st.session_state:
        st.session_state.user_authenticated = False

    if st.session_state.user_authenticated:
        return True

    # Show login form
    st.title(":material/key_vertical: SRKW Salmon Signals Login")
    st.markdown("---")

    # Show locked message
    st.markdown(
        """
        ## :material/account_circle: Admin Access
        Please enter the username and password to access SRKW Salmon Signals application.

        To request login information, please reach out to **Tyler** at [stevetylda@gmail.com](mailto:stevetylda@gmail.com) or via the OrcaSound Zulip chat.
        """,
        unsafe_allow_html=False,
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == GENERAL_USERNAME and password == GENERAL_PASSWORD:
            st.session_state.user_authenticated = True
            st.rerun()
        else:
            st.error("❌ Incorrect username or password.")

    return False
