import os
import yt_dlp
import imageio_ffmpeg as ffmpeg
import streamlit as st

# Get the path to the ffmpeg binary from imageio-ffmpeg
ffmpeg_path = ffmpeg.get_ffmpeg_exe()

# Ensure the output directory exists
output_dir = 'downloads'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

st.title("YouTube Video Downloader")
video_url = st.text_input("YouTube Video URL", "")

if video_url:
    try:
        st.write("Processing video...")

        # Configure yt-dlp to use the ffmpeg path directly and sanitize filename
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Best video and audio streams
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Save to 'downloads' folder
            'ffmpeg_location': ffmpeg_path,  # Set ffmpeg location directly here
            'merge_output_format': 'mp4',  # Directly merge to mp4 instead of webm
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            sanitized_title = sanitize_filename(info['title'])
            st.write(f"**Title:** {sanitized_title}")
            st.write(f"**Duration:** {info['duration']} seconds")
            st.write(f"**Views:** {info['view_count']}")

            # Update the filename with sanitized title
            ydl_opts['outtmpl'] = os.path.join(output_dir, f"{sanitized_title}.%(ext)s")

            # Download video on button click
            if st.button("Download Video"):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                st.success(f"Download completed! Check the '{output_dir}' folder.")
    except Exception as e:
        st.error(f"An error occurred: {e}")