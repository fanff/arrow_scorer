import streamlit as st
from db import SessionLocal
from models import Session
import matplotlib.pyplot as plt

db = SessionLocal()

if "selected_session_id" not in st.session_state:
    st.error("No session selected.")
    st.stop()

s = db.query(Session).filter_by(id=st.session_state["selected_session_id"]).first()
st.title("📊 Session Review")
st.markdown(f"**Date:** {s.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

# Collect all arrows
arrows = [a for set in s.sets for a in set.arrows]

# Statistics
st.subheader("Statistics")
if not arrows:
    st.info("No data available.")
else:
    avg_score = sum(a.score for a in arrows) / len(arrows)
    st.write(f"**Total Arrows:** {len(arrows)}")
    st.write(f"**Average Score:** {avg_score:.2f}")

    # Plot
    st.subheader("Arrow Position Plot")
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_title("Arrow Impact Points")

    xs = [a.x for a in arrows]
    ys = [a.y for a in arrows]
    scores = [a.score for a in arrows]

    scatter = ax.scatter(xs, ys, c=scores, cmap='viridis', s=100, edgecolor='black')
    plt.colorbar(scatter, label="Score")
    st.pyplot(fig)
