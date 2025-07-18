
import base64
import streamlit as st
from db import SessionLocal
from models import Session, ArrowSet, Arrow
import pandas as pd
from PIL import Image, ImageDraw
import io
import math
import streamlit.components.v1 as components
TARGET_SIZE = 100  # px

def draw_target_with_arrow(x=None, y=None):
    img = Image.new("RGB", (TARGET_SIZE, TARGET_SIZE), "white")
    draw = ImageDraw.Draw(img)

    center = (TARGET_SIZE // 2, TARGET_SIZE // 2)
    colors = ["blue", "red", "red", "gold", "gold" ]

    # Draw 5 concentric circles
    for i, color in enumerate(colors):
        r = len(colors) - i
        r *= 10
        draw.ellipse(
            [center[0] - r, center[1] - r, center[0] + r, center[1] + r],
            outline="black",
            fill=color,
        )

    # Draw the clicked point
    if x is not None and y is not None:
        r = 3
        px = int(center[0] + (x*TARGET_SIZE/2))
        py = int(center[1] - (y*TARGET_SIZE/2))
        draw.ellipse([px - r, py - r, px + r, py + r], fill="black")
    
    return img

from streamlit_drawable_canvas import st_canvas
def arrow_input(arrow_index):
    st.markdown(f"### Arrow {arrow_index+1}")
    coords = [0,0]
    col1, col2 = st.columns([2,1])
    with col1:
        click_x = st.slider("X", -5.0, 5.0, .0, key=f"x_{arrow_index}", step=0.1,label_visibility="collapsed")
        click_y = st.slider("Y", -5.0, 5.0, .0, key=f"y_{arrow_index}", step=0.1,label_visibility="collapsed")
        score = st.radio(f"Score for Arrow {arrow_index+1}", options=[10, 9, 8, 7, 6], key=f"score_{arrow_index}",horizontal=True,label_visibility="collapsed")
        
    if score:
        pass 
        #st.write(f"Arrow with score {score}")
    if click_x:
        coords = [click_x / 5.0, click_y / 5.0]
    if click_y:
        coords = [click_x / 5.0, click_y / 5.0]

    with col2:
        image = draw_target_with_arrow(*coords)
        #base64_img = base64.b64encode(buf.getvalue()).decode()
        st.image(image)
    #st.write(f"{coords}")
    
    return click_x,click_y,score # scale to match -10..+10 range

results = []
for i in range(4):
    results.append(arrow_input(i))
if st.button("Add Set"):
    st.write("Adding set with results:", results)
    

