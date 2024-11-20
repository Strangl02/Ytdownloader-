import os
from yt_dlp import YoutubeDL
from yt_dlp.utils import sanitize_filename
import imageio_ffmpeg as ffmpeg
import streamlit as st

# Get ffmpeg path
ffmpeg_path = ffmpeg.get_ffmpeg_exe()

# Create downloads folder
output_dir = 'downloads'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

st.title("YouTube Video Downloader")
video_url = st.text_input("YouTube Video URL", "")

if video_url:
    if not video_url.startswith("http"):
        st.error("Please enter a valid YouTube URL.")
    else:
        try:
            st.write("Processing video...")

            # Configure yt-dlp
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'ffmpeg_location': ffmpeg_path,
                'merge_output_format': 'mp4',
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)

                if isinstance(info, dict):
                    sanitized_title = sanitize_filename(info['title'])
                    st.write(f"**Title:** {sanitized_title}")
                    st.write(f"**Duration:** {info['duration']} seconds")
                    st.write(f"**Views:** {info['view_count']}")

                    ydl_opts['outtmpl'] = os.path.join(output_dir, f"{sanitized_title}.%(ext)s")

                    if st.button("Download Video"):
                        ydl.download([video_url])
                        st.success(f"Download completed! Check the '{output_dir}' folder.")
                else:
                    st.error("Unable to retrieve video metadata.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
