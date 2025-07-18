import streamlit as st
from db import SessionLocal
from models import Session, ArrowSet, Arrow
import pandas as pd
from streamlit_drawable_canvas import st_canvas,CanvasResult
from PIL import Image, ImageDraw
import io
import math

db = SessionLocal()

if "selected_session_id" not in st.session_state:
    st.error("No session selected.")
    st.stop()

session_id = st.session_state["selected_session_id"]
s:Session = db.query(Session).filter_by(id=session_id).first()

st.title("🎯 Edit Session")
st.markdown(f"**Date:** {s.timestamp.strftime('%Y-%m-%d %H:%M:%S')}  |  **Arrows/Set:** {s.arrows_per_set}")

# Show existing sets
st.subheader("Previous Sets")
all_scores = []
for i, arrow_set in enumerate(s.sets, start=1):
    all_scores.append([a.score for a in arrow_set.arrows])


df = pd.DataFrame(all_scores, columns=[f"Arrow {i+1}" for i in range(s.arrows_per_set)])
st.table(df)


# Add new set
st.subheader("Add New Set")
coords = []
scores = []



TARGET_SIZE = 100  # px

def draw_target_with_arrow(x=None, y=None):
    img = Image.new("RGB", (TARGET_SIZE, TARGET_SIZE), "white")
    draw = ImageDraw.Draw(img)

    center = (TARGET_SIZE // 2, TARGET_SIZE // 2)
    colors = ["gold", "red", "blue", "black", "white"]

    # Draw 5 concentric circles
    for i, color in enumerate(colors[::-1], start=1):
        r = i * 10
        draw.ellipse(
            [center[0] - r, center[1] - r, center[0] + r, center[1] + r],
            outline="black",
            fill=color,
        )

    # Draw the clicked point
    if x is not None and y is not None:
        r = 2
        px = int(center[0] + x)
        py = int(center[1] - y)
        draw.ellipse([px - r, py - r, px + r, py + r], fill="black")

    return img



def arrow_input(arrow_index):
    st.markdown(f"### Arrow {arrow_index+1}")
    
    click_x = st.slider(f"X position (px)", -50, 50, 0, key=f"x_{arrow_index}")
    click_y = st.slider(f"Y position (px)", -50, 50, 0, key=f"y_{arrow_index}")
    
    img = draw_target_with_arrow(click_x, click_y)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    st.image(buf.getvalue(), width=100)

    score = st.radio(f"Score for Arrow {arrow_index+1}", options=[10, 9, 8, 7, 6], key=f"score_{arrow_index}")
    
    return click_x / 5.0, click_y / 5.0, score  # scale to match -10..+10 range









with st.form("add_set"):
    
    st.write("Click the target to add arrow positions")
    coords = []
    scores = []
    for i in range(s.arrows_per_set):
        x, y, score = arrow_input(i)
        coords.append((x, y))
        scores.append(score)
        

    if st.form_submit_button("Add Set"):
        new_set = ArrowSet(session_id=s.id)
        db.add(new_set)
        db.flush()

        for (x, y), score in zip(st.session_state["arrow_positions"], st.session_state["arrow_scores"]):
            db.add(Arrow(set_id=new_set.id, x=x, y=y, score=score))

        db.commit()
        st.success("Set added.")
        st.session_state["arrow_positions"] = []
        st.session_state["arrow_scores"] = []
        st.rerun()