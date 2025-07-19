import streamlit as st
from db import init_db, SessionLocal
from models import Session
from datetime import datetime


from auth import ENABLE_AUTH, check_auth

if ENABLE_AUTH:
    if not check_auth():
        st.stop()

init_db()
db = SessionLocal()

st.title("🏹 Archery Training Tracker")

# Load sessions
sessions = db.query(Session).order_by(Session.timestamp.desc()).all()

# Session table
st.subheader("Existing Sessions")
for s in sessions:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(
            f"**{s.timestamp.strftime('%Y-%m-%d %H:%M:%S')}** - {s.arrows_per_set} arrows/set"
        )
    with col2:
        if st.button("Continue", key=f"edit_{s.id}"):
            st.session_state["selected_session_id"] = s.id
            st.switch_page("pages/Session_Editor.py")
    with col3:
        if st.button("Review", key=f"review_{s.id}"):
            st.session_state["selected_session_id"] = s.id
            st.switch_page("pages/Session_Review.py")

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
