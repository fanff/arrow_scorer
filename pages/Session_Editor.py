import streamlit as st
from auth import ENABLE_AUTH, check_auth
from css_addon import custom_css
from db import SessionLocal
from models import Session, ArrowSet, Arrow
from PIL import Image, ImageDraw
import math

from utils import arrow_score_df

if ENABLE_AUTH:
    if not check_auth():
        st.stop()
custom_css()

SLIDER_MIN_MAX = 5.0
TARGET_SIZE = 100  # px


def draw_target_with_arrow(x=None, y=None):
    img = Image.new("RGBA", (TARGET_SIZE, TARGET_SIZE), color="#00000000")
    draw = ImageDraw.Draw(img)

    center = (TARGET_SIZE // 2, TARGET_SIZE // 2)
    colors = ["blue", "red", "red", "gold", "gold"]

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
        px = int(center[0] + (x * TARGET_SIZE / 2))
        py = int(center[1] - (y * TARGET_SIZE / 2))
        draw.ellipse([px - r, py - r, px + r, py + r], fill="black")

    return img


def xy_to_points(x, y):
    """Convert x,y coordinates to arrow score point between 6 to 10."""
    if x is None or y is None:
        return 0
    distance = math.sqrt(x**2 + y**2)
    if distance < 1.0:
        return 10
    elif distance < 2.0:
        return 9
    elif distance < 3.0:
        return 8
    elif distance < 4.0:
        return 7
    elif distance < 5.0:
        return 6
    else:
        return 0


def arrow_input(arrow_index):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### Arrow {arrow_index + 1}")
    with col2:
        spot_number = st.selectbox(
            "Spot",
            options=[1, 2, 3],
            index=arrow_index % 3,
        key=f"arrow_spot_{arrow_index}",
        label_visibility="collapsed",
    )
    coords = [0, 0]
    click_x = st.slider(
        "X",
        -SLIDER_MIN_MAX,
        SLIDER_MIN_MAX,
        0.0,
        key=f"x_{arrow_index}",
        step=0.1,
        label_visibility="collapsed",
    )
    click_y = st.slider(
        "Y",
        -SLIDER_MIN_MAX,
        SLIDER_MIN_MAX,
        0.0,
        key=f"y_{arrow_index}",
        step=0.1,
        label_visibility="collapsed",
    )
    # add a hidden input to store the score
    points = 0
    if click_x:
        points = xy_to_points(click_x, click_y)
        coords = [click_x / SLIDER_MIN_MAX, click_y / SLIDER_MIN_MAX]
    if click_y:
        points = xy_to_points(click_x, click_y)
        coords = [click_x / SLIDER_MIN_MAX, click_y / SLIDER_MIN_MAX]

    col2, col3 = st.columns(2)

    with col2:
        image = draw_target_with_arrow(*coords)
        st.image(image, channels="RGBA", use_container_width="always")
    with col3:
        st.markdown(f"# {points}")

    return click_x, click_y, spot_number


db = SessionLocal()

if "selected_session_id" not in st.session_state:
    st.switch_page("main.py")

session_id = st.session_state["selected_session_id"]
s: Session = db.query(Session).filter_by(id=session_id).first()
if not s:
    st.switch_page("main.py")

(col1, col2) = st.columns([1, 1])
with col1:
    if st.button(" <<", icon="🏹"):
        st.session_state["selected_session_id"] = None
        st.switch_page("main.py")

with col2:
    if st.button("Review Session", icon="🔍"):
        st.session_state["selected_session_id"] = session_id
        st.switch_page("pages/Session_Review.py")


st.title(f"🎯 {s.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown(f"**Arrows/Set:** {s.arrows_per_set}")

# TODO add a text area for notes
# st.text_area("Notes", value="", key="session_notes", height=100)

# Show existing sets
st.subheader("Previous Sets")
st.table(arrow_score_df(s))

# horizontal line accoss the page
st.markdown("---")

# Add new set
results = []
for i in range(s.arrows_per_set):
    results.append(arrow_input(i))

if st.button("Add Set"):

    new_set = ArrowSet(session_id=s.id)
    db.add(new_set)
    db.flush()

    for x, y, spot in results:
        score = xy_to_points(x, y)
        a = Arrow(set_id=new_set.id, x=x, y=y, score=score, spot=spot)
        db.add(a)

    db.commit()
    st.success("Set added.")
    st.rerun()
