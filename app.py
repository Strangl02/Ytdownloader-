import streamlit as st
import yt_dlp

st.title("YouTube Video Downloader")
video_url = st.text_input("YouTube Video URL", "")

if video_url:
    try:
        st.write("Processing video...")

        # Configure yt-dlp
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',  # Save with video title as the filename
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            st.write(f"**Title:** {info['title']}")
            st.write(f"**Duration:** {info['duration']} seconds")
            st.write(f"**Views:** {info['view_count']}")

            # Download video on button click
            if st.button("Download Video"):
                ydl.download([video_url])
                st.success("Download completed!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
