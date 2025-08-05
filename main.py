import streamlit as st
from css_addon import custom_css
from db import init_db, SessionLocal
from models import Session
from datetime import datetime


from auth import ENABLE_AUTH, check_auth, get_authenticator
from utils import draw_target_with_arrow

is_authenticated, authenticator = check_auth()
authenticator.logout()

custom_css()

init_db()

db = SessionLocal()

st.title("🏹 Archery Score Tracker")

# Load sessions
sessions = db.query(Session).order_by(Session.timestamp.desc()).all()

# Session table
st.subheader("Existing Sessions")
for s in sessions:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"**{s.timestamp.strftime('%Y-%m-%d %H:%M')}**\n\n{s.arrows_per_set} arrows/set",
            width="content",
        )
    with col2:
        if st.button("Edit", key=f"edit_{s.id}", icon="✏️"):
            st.session_state["selected_session_id"] = s.id
            st.switch_page("pages/Session_Editor.py")
    with col3:
        if st.button("Review", key=f"review_{s.id}", icon="🔎"):
            st.session_state["selected_session_id"] = s.id
            st.switch_page("pages/Session_Review.py")
    st.markdown("---")
# Create new session
st.subheader("Create New Session")
with st.form("new_session"):
    arrows_per_set = st.number_input(
        "Number of arrows per set", min_value=1, max_value=12, value=6
    )
    if st.form_submit_button("Create Session"):
        new_s = Session(arrows_per_set=arrows_per_set)
        db.add(new_s)
        db.commit()
        st.session_state["selected_session_id"] = new_s.id
        st.success("Session created!")
        st.switch_page("pages/Session_Editor.py")

