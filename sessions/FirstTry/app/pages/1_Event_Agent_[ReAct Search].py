import streamlit as st
import requests
from .. import config
from .. import ui

st.set_page_config(layout="wide")
ui.inject_global_css()

# Header
title = config.APP_NAME
logo_path = config.get_logo_path()

if "event_response" not in st.session_state:
    st.session_state.event_response = ""

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

# Set up the main app page
st.subheader("Discover your next local athletic event!")
st.write("For example, I can help you find a 10k marathon event at San Francisco in August.")


with st.form(key='event_form'):
    event_type = st.text_input("Type of event")
    location = st.text_input("Location")
    time_frame = st.text_input("Month")
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    payload = {
            "event_type": event_type,
            "location": location,
            "time_frame": time_frame
        }
    
    with st.spinner(f'Looking for {location} {event_type} in {time_frame}...'):
        response = requests.post(f"{config.BACKEND_URL}/event", json=payload).json()
        st.session_state.event_response = response["response"]
    
# display output
st.write(st.session_state.event_response)
    