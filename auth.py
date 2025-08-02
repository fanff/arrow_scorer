
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



import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader


def get_authenticator():
    authentication_config_file = os.getenv("AUTHENTICATION_CONFIG_FILE", "./config.yaml")
    with open(authentication_config_file) as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Pre-hashing all plain text passwords once
    # stauth.Hasher.hash_passwords(config['credentials'])

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    return authenticator

def check_auth():
    authenticator = get_authenticator()
    authenticator.login()
    if st.session_state.get('authentication_status'):
        return True, authenticator
    elif st.session_state.get('authentication_status') is False:
        st.error('Username/password is incorrect')
        st.stop()
        return False, authenticator
    elif st.session_state.get('authentication_status') is None:
        st.warning('Please enter your username and password')
        st.stop()
        return False, authenticator