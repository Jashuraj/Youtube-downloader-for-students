import yt_dlp
import streamlit as st
import os

# Function to download the playlist with progress
def download_playlist(url, resolution, download_path):
    # Progress hook to track download progress
    def progress_hook(d):
        if d['status'] == 'downloading':
            # Extract the download percentage and speed
            percentage = d['downloaded_bytes'] / d['total_bytes'] * 100 if d['total_bytes'] else 0
            speed = d.get('speed', 0)
            downloaded_size = d['downloaded_bytes']

            # Update progress bar and display current status
            st.session_state.progress_bar.progress(percentage / 100)  # Set the progress bar
            st.session_state.progress_text.text(f"Downloaded: {percentage:.2f}%")

            # Show download speed and size
            st.session_state.speed_text.text(f"Speed: {format_speed(speed)}")
            st.session_state.size_text.text(f"Downloaded: {format_size(downloaded_size)} / Total Size: {format_size(d['total_bytes'])}")

        elif d['status'] == 'finished':
            # When the download finishes
            st.session_state.progress_bar.progress(1)  # Set the progress bar to 100%
            st.session_state.progress_text.text(f"Download complete!")

    # Format the speed in a human-readable way
    def format_speed(speed):
        if speed < 1024:
            return f"{speed} B/s"
        elif speed < 1024**2:
            return f"{speed / 1024:.2f} KB/s"
        else:
            return f"{speed / 1024**2:.2f} MB/s"

    # Format the size in a human-readable way
    def format_size(size):
        if size < 1024:
            return f"{size} B"
        elif size < 1024**2:
            return f"{size / 1024:.2f} KB"
        elif size < 1024**3:
            return f"{size / 1024**2:.2f} MB"
        else:
            return f"{size / 1024**3:.2f} GB"

    # Download options
    ydl_opts = {
        "format": f"bv*[height={resolution}]+ba/best",  # Select video resolution and best audio
        "merge_output_format": "mp4",  # Ensure MP4 output
        "outtmpl": os.path.join(download_path, "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"),  # Organize into playlist folder
        "noplaylist": False,  # Allow playlist downloading
        "retries": 10,  # Retry up to 10 times for failed downloads
        "fragment_retries": 10,  # Retry failed video fragments
        "continue": True,  # Resume interrupted downloads
        "ignoreerrors": True,  # Skip failed videos instead of stopping
        "buffersize": 16 * 1024,  # Set buffer size to 16 KB for stability
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",  # Convert output to MP4
            }
        ],
        "progress_hooks": [progress_hook],  # Add the progress hook to track download progress
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  # Start downloading the playlist
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit UI
def main():
    # Streamlit setup
    st.title("YouTube Video/Playlist Downloader")
    st.info("NOTE:Works For Laptop/Pc Only")

    # Input for YouTube playlist URL
    playlist_url = st.text_input("Enter YouTube Video/Playlist URL:")

    # Resolution selection
    resolution = st.selectbox("Select Resolution:", ["360", "480", "720", "1080"], index=3)

    # Path input for download location
    download_path = st.text_input("Enter Download Path:", value=os.getcwd())

    # Show the download progress in the form of a progress bar and text
    st.session_state.progress_bar = st.progress(0)  # Initialize the progress bar
    st.session_state.progress_text = st.empty()  # Initialize empty space for the text
    st.session_state.speed_text = st.empty()  # Initialize empty space for the speed text
    st.session_state.size_text = st.empty()  # Initialize empty space for the size text

    # Button to trigger download
    if st.button("Download"):
        if playlist_url and download_path:
            # Check if the provided path exists, if not create the directory
            if not os.path.exists(download_path):
                os.makedirs(download_path)
                st.write(f"Created The Directory: {download_path}")

            st.write(f"Downloading Video/Playlist From: {playlist_url} at {resolution}p to {download_path}")
            download_playlist(playlist_url, resolution, download_path)
        else:
            st.error("Please Enter A Valid Playlist URL And Download Path.")

    st.sidebar.subheader("👨🏻‍💻Developed By👨🏻‍💻")
    st.sidebar.subheader("⚡JASHWANTH RAJ J.R")
    st.sidebar.subheader("")
    st.sidebar.subheader("📚EDUCATIONAL PURPOSE ONLY🖋️")
    st.sidebar.subheader("")
    st.sidebar.subheader("⚠️Disclimer:")
    st.sidebar.subheader("1.Copyright Compliance: This tool is provided for educational and personal use only. By using this tool, you agree to comply with all applicable copyright laws and guidelines. Downloading copyrighted content without permission from the content owner may violate copyright laws. Please ensure that you have the right to download and use the content you are accessing.")
    st.sidebar.subheader("2.Responsibility: The developer of this tool (Jashwanth Raj J.R) is not responsible for any content downloaded, including any legal issues that may arise. Users of this tool are solely responsible for ensuring that their actions comply with the laws of their respective jurisdictions.")
    st.sidebar.subheader("3.Content Ownership: This tool is intended to assist in downloading publicly available videos, such as content with open licenses or non-copyrighted material. The tool does not support or encourage downloading paid or protected content without the express permission of the content owner.")
    st.sidebar.subheader("4.No Liability: The creator of this tool does not accept any liability for loss of data, damage to devices, or legal consequences caused by improper use of this tool. By using this tool, you agree to indemnify the developer from any damages or legal action resulting from its use.")
    st.sidebar.subheader("5.Terms of Service: You are advised to review and comply with the terms of service of any platform you download content from (e.g., YouTube, Vimeo, etc.). This tool does not circumvent any platform’s terms or guidelines.")

if __name__ == "__main__":
    main()
