import os
import re
import streamlit as st
import yt_dlp
import imageio_ffmpeg as ffmpeg

# Get the path to the ffmpeg binary from imageio-ffmpeg
ffmpeg_path = ffmpeg.get_ffmpeg_exe()

# Function to sanitize the filename
def sanitize_filename(filename):
    # Remove any special characters and replace with underscore
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)  # Remove invalid characters
    filename = re.sub(r'\s+', '_', filename)  # Replace spaces with underscores
    return filename

st.title("YouTube Video Downloader")
video_url = st.text_input("YouTube Video URL", "")

if video_url:
    try:
        st.write("Processing video...")

        # Configure yt-dlp to use the ffmpeg path directly and sanitize filename
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',  # Save with video title as the filename
            'ffmpeg_location': ffmpeg_path,  # Set ffmpeg location directly here
            'postprocessors': [
                {
                    'key': 'FFmpegMerger',  # Merge video and audio
                }
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            sanitized_title = sanitize_filename(info['title'])
            st.write(f"**Title:** {sanitized_title}")
            st.write(f"**Duration:** {info['duration']} seconds")
            st.write(f"**Views:** {info['view_count']}")

            # Update the filename with sanitized title
            ydl_opts['outtmpl'] = f"{sanitized_title}.%(ext)s"

            # Download video on button click
            if st.button("Download Video"):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                st.success("Download completed!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
