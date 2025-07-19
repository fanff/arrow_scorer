# Optional Auth Configuration
import os
import streamlit as st

ENABLE_AUTH = os.getenv("ENABLE_AUTH", "False") == "True"
USERNAME = os.getenv("APP_USERNAME", "admin")
PASSWORD = os.getenv("APP_PASSWORD", "password")


def check_auth():
    """Simple auth form"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.form("Login"):
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if user == USERNAME and pwd == PASSWORD:
                    st.session_state.authenticated = True
                    st.success("Logged in successfully")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        return False
    return True
