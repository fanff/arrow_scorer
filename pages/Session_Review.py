import streamlit as st
from auth import ENABLE_AUTH, check_auth
from css_addon import custom_css
from db import SessionLocal
from models import Session
import matplotlib.pyplot as plt
import numpy as np
from utils import mark_sheet_df, arrow_scores_df, plot_pos


from utils import pos_to_score_range

if ENABLE_AUTH:
    if not check_auth():
        st.stop()

custom_css()


db = SessionLocal()

if "selected_session_id" not in st.session_state:
    st.switch_page("main.py")

session_id = st.session_state["selected_session_id"]
current_session = db.query(Session).filter_by(id=session_id).first()

if not current_session:
    st.switch_page("main.py")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button(" ", icon="⬅️"):
        st.session_state["selected_session_id"] = None
        st.switch_page("main.py")

with col2:
    if st.button("Continue Session", icon="▶️"):
        st.session_state["selected_session_id"] = session_id
        st.switch_page("pages/Session_Editor.py")


st.title("📊 Session Review")
st.markdown(f"**Date:** {current_session.timestamp.strftime('%Y-%m-%d %H:%M')}")

# Collect all arrows
arrows = [a for set in current_session.sets for a in set.arrows]

# Score
st.subheader("Score Board")
if not arrows:
    st.info("No data available.")
else:
    asdf = mark_sheet_df(current_session)
    st.table(asdf)

    avg_score = sum(a.score for a in arrows) / len(arrows)
    std_score = np.std([a.score for a in arrows])
    fig, mu_x, std_x, mu_y, std_y = plot_pos(arrows)
    estimated_score = 60 * avg_score

    # Fancy metrics display
    st.markdown("### Key Metrics")
    with st.container():
        col2, col3 = st.columns(2)
        col2.metric("Avg. Score", f"{avg_score:.2f}")
        col3.metric("Est. 60 Arrow Score", f"{estimated_score:.2f}")

    col4, col5 = st.columns(2)
    col4.metric("Avg. X Position", f"{pos_to_score_range(mu_x):.2f}")
    col5.metric(
        "Avg. Y Position",
        f"{pos_to_score_range(mu_y):.2f}",
    )

    # Plot
    st.subheader("Arrow Position Plot")
    st.pyplot(fig)

# Convert to DataFrame
asdf = arrow_scores_df(current_session)

st.subheader("Spot Details")

st.table(asdf.groupby("spot").mean(["score", "x", "y"])[["score", "x", "y"]])



# export button 
st.subheader("Export Data")



# Create download link
st.download_button(
    label="Download CSV",
    data=asdf.to_csv(index=False),
    file_name=f"session_{current_session.id}_data.csv",
    mime="text/csv",
)