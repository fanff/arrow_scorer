import streamlit as st
from db import SessionLocal
from models import Session
import matplotlib.pyplot as plt

from utils import arrow_score_df, plot_pos

db = SessionLocal()

if "selected_session_id" not in st.session_state:
    st.error("No session selected.")
    st.stop()


session_id = st.session_state["selected_session_id"]
s = db.query(Session).filter_by(id=session_id).first()



(col1, col2) = st.columns([1,1]) 
with col1:
    if st.button(" < Back to Main"):
        st.session_state["selected_session_id"] = None
        st.switch_page("main.py")

with col2:
    if st.button("Continue Session"):
        st.session_state["selected_session_id"] = session_id
        st.switch_page("pages/Session_Editor.py")

        
st.title("📊 Session Review")
st.markdown(f"**Date:** {s.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

# Collect all arrows
arrows = [a for set in s.sets for a in set.arrows]

# Statistics
st.subheader("Statistics")
if not arrows:
    st.info("No data available.")
else:
    df = arrow_score_df(s)
    st.table(df)

    avg_score = sum(a.score for a in arrows) / len(arrows)
    st.write(f"**Total Arrows:** {len(arrows)}")
    st.write(f"**Average Score:** {avg_score:.2f}")

    # Plot
    st.subheader("Arrow Position Plot")
    fig = plot_pos(arrows)
    st.pyplot(fig)
