# streamlit_video_app.py

import streamlit as st
from get_video import get_latest_video_base64  # Import the function from get_video.py
import base64
from io import BytesIO

# Streamlit app layout
st.title("Latest Video from Crash Cam")

# Get the latest video data from MongoDB
video_base64 = get_latest_video_base64()
print(video_base64)

if video_base64:
    # Decode the Base64 string and convert it to bytes
    video_data = base64.b64decode(video_base64)
    with open('video.mp4', 'wb') as f:
        f.write(video_data)

    # Create a BytesIO object and display the video
    # video_bytes = BytesIO(video_data)
    st.video('video.mp4', format="video/mp4", start_time=0)  # Adjust the format if necessary
else:
    st.error("Unable to retrieve the video.")

# Run the Streamlit app using the command below:
# streamlit run streamlit_video_app.py
