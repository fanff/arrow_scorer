import streamlit as st
from db import SessionLocal
from models import Session, ArrowSet, Arrow

db = SessionLocal()

if "selected_session_id" not in st.session_state:
    st.error("No session selected.")
    st.stop()

session_id = st.session_state["selected_session_id"]
s = db.query(Session).filter_by(id=session_id).first()

st.title("🎯 Edit Session")
st.markdown(f"**Date:** {s.timestamp.strftime('%Y-%m-%d %H:%M:%S')}  |  **Arrows/Set:** {s.arrows_per_set}")

# Show existing sets
st.subheader("Previous Sets")
for i, arrow_set in enumerate(s.sets, start=1):
    scores = [a.score for a in arrow_set.arrows]
    st.write(f"Set {i}: {scores} (Total: {sum(scores)})")

# Add new set
st.subheader("Add New Set")
coords = []
scores = []

with st.form("add_set"):
    for i in range(s.arrows_per_set):
        col1, col2, col3 = st.columns(3)
        with col1:
            x = st.number_input(f"Arrow {i+1} X", key=f"x{i}")
        with col2:
            y = st.number_input(f"Arrow {i+1} Y", key=f"y{i}")
        with col3:
            score = st.number_input(f"Score {i+1}", min_value=0, max_value=10, key=f"score{i}")
        coords.append((x, y))
        scores.append(score)

    if st.form_submit_button("Add Set"):
        new_set = ArrowSet(session_id=s.id)
        db.add(new_set)
        db.flush()  # get ID before commit

        for (x, y), score in zip(coords, scores):
            db.add(Arrow(set_id=new_set.id, x=x, y=y, score=score))

        db.commit()
        st.success("Set added.")
        st.experimental_rerun()
