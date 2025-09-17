import streamlit as st
import requests
from .. import config
from .. import ui

st.set_page_config(layout="wide")
ui.inject_global_css()

# Header
title = config.APP_NAME
logo_path = config.get_logo_path()

if "nutrition_response" not in st.session_state:
    st.session_state.nutrition_response = ""

col1, col2 = st.columns([1, 10])

with col1:
    if logo_path:
        st.image(logo_path, width=100)

# Display the title in the second column
with col2:
    st.title(title)

if (st.session_state.get("password_correct") == None) or (st.session_state.get("password_correct") == False):
    st.write("Please login first.")
    st.stop()

st.subheader("Find specific meal options based on your diet (e.g., Mediterranean, Keto, Vegan, etc.)!")
user_input = st.text_input(label="nutrition_agent", label_visibility="hidden", placeholder="What are some Mediterranean breakfast options?")

# button to submit request
if st.button("Request nutrition options"):
    with st.spinner(f'Retrieving...'):
        data = requests.post(f"{config.BACKEND_URL}/nutrition", json={"query": user_input}).json()
        st.session_state.nutrition_response = data["response"]
    
st.write(st.session_state.nutrition_response)
