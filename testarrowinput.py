
import base64
import streamlit as st
from db import SessionLocal
from models import Session, ArrowSet, Arrow
import pandas as pd
from PIL import Image, ImageDraw
import io
import math
import streamlit.components.v1 as components


results = []
for i in range(4):
    results.append(arrow_input(i))
if st.button("Add Set"):
    st.write("Adding set with results:", results)
    

