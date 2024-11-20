import os
import streamlit as st
import yt_dlp
import imageio_ffmpeg as ffmpeg

# Get the path to the ffmpeg binary from imageio-ffmpeg
ffmpeg_path = ffmpeg.get_ffmpeg_exe()

st.title("YouTube Video Downloader")
video_url = st.text_input("YouTube Video URL", "")

if video_url:
    try:
        st.write("Processing video...")

        # Configure yt-dlp to use the ffmpeg path
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',  # Save with video title as the filename
            'postprocessors': [
                {
                    'key': 'FFmpegVideoConvertor',
                    'prefer_ffmpeg': True,
                    'ffmpeg_location': ffmpeg_path,  # Explicitly set ffmpeg path
                }
            ],
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
