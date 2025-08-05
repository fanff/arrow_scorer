import datetime
import os
import streamlit as st
from streamlit_image_coordinates  import streamlit_image_coordinates
from auth import check_auth
from css_addon import custom_css
from db import SessionLocal
from models import Session, ArrowSet, Arrow

import math

from utils import draw_target_with_arrow, mark_sheet_df

is_authenticated, authenticator = check_auth()
authenticator.logout()
custom_css()

SLIDER_MIN_MAX = 5.0

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
    target_size=200

    col1, col2, col3 = st.columns(3)
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
    
    def add_point():
        value = st.session_state[f"score_{arrow_index}"]
        x = value["x"]
        y = value["y"]
        # normalize the coordinates with the image size
        x = (x - value["width"] // 2) / (value["width"] // 2)
        y = (value["height"] // 2 - y) / (value["height"] // 2)
        # set the x & y in the session state
        st.session_state[f"px_{arrow_index}"] = x
        st.session_state[f"py_{arrow_index}"] = y
        
    coords  = [st.session_state.get(f"px_{arrow_index}",default=0),
                st.session_state.get(f"py_{arrow_index}", default=0)]
    points = xy_to_points(coords[0]*5, coords[1]*5)
    with col3:
        points= st.write(f"### {points}")

    img = draw_target_with_arrow(*coords, target_size=target_size)

    # Draw the target with the arrow coordinates
    # and get the click coordinates
    streamlit_image_coordinates(
        img,
        key=f"score_{arrow_index}",
        use_column_width=True,
        on_click=add_point,
    )

    return (coords[0], coords[1],
            spot_number)



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
st.table(mark_sheet_df(s))

# horizontal line accoss the page
st.markdown("---")

# Add new set
results = []
for i in range(s.arrows_per_set):
    results.append(arrow_input(i))

if st.button("Add Set"):

    new_set = ArrowSet(session_id=s.id, timestamp=datetime.datetime.now(datetime.timezone.utc))
    db.add(new_set)
    db.flush()

    for x, y, spot in results:
        score = xy_to_points(x*5, y*5)
        a = Arrow(set_id=new_set.id, x=x*5, y=y*5, score=score, spot=spot)
        db.add(a)

    db.commit()
    st.success("Set added.")
    st.rerun()


# File uploader
uploaded_files = st.file_uploader("Choose a file to upload", type=None, accept_multiple_files=True)


if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        # Show file details
        st.subheader("File Details:")
        st.write(f"Filename: {uploaded_file.name}")
        st.write(f"File type: {uploaded_file.type}")
        st.write(f"File size: {uploaded_file.size / (1024 * 1024):.2f} MB")

        # Save uploaded file to disk
        os.makedirs("uploads", exist_ok=True)
       
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
        base, ext = os.path.splitext(uploaded_file.name)
        save_path = os.path.join("uploads", f"{base}_{timestamp}{ext}")
        # Save the file
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
       
        st.success(f"File saved to: {save_path}")
