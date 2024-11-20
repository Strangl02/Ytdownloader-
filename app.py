import streamlit as st
from pytube import YouTube

# Title and instructions
st.title("YouTube Video Downloader")
st.write("Enter the YouTube video link below to download the video in the highest resolution.")

# Input field for the YouTube link
video_url = st.text_input("YouTube Video URL", "")

if video_url:
    try:
        # Process the YouTube video
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()

        st.write(f"**Title:** {yt.title}")
        st.write(f"**Duration:** {yt.length} seconds")
        st.write(f"**Views:** {yt.views}")
        st.write("Click the button below to download the video:")

        # Button to download the video
        if st.button("Download Video"):
            stream.download()
            st.success("Download completed!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
