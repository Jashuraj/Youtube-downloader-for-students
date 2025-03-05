import yt_dlp
import streamlit as st
import os

# Get default Downloads folder
default_download_path = os.path.join(os.path.expanduser("~"), "Downloads")

# Function to download the playlist with progress
def download_playlist(url, resolution, download_path):
    # Progress hook to track download progress
    def progress_hook(d):
        downloaded_bytes = d.get('downloaded_bytes', 0)
        total_bytes = d.get('total_bytes', 0)
        speed = d.get('speed', 0)

        if d['status'] == 'downloading':
            percentage = (downloaded_bytes / total_bytes) * 100 if total_bytes > 0 else 0
            st.session_state.progress_bar.progress(percentage / 100)
            st.session_state.progress_text.text(f"Downloaded: {percentage:.2f}%")
            st.session_state.speed_text.text(f"Speed: {format_speed(speed)}")
            st.session_state.size_text.text(f"Downloaded: {format_size(downloaded_bytes)} / Total Size: {format_size(total_bytes)}")
        elif d['status'] == 'finished':
            st.session_state.progress_bar.progress(1)
            st.session_state.progress_text.text("Download complete!")

    def format_speed(speed):
        if speed is None:
            return "Unknown"
        elif speed < 1024:
            return f"{speed} B/s"
        elif speed < 1024**2:
            return f"{speed / 1024:.2f} KB/s"
        else:
            return f"{speed / 1024**2:.2f} MB/s"

    def format_size(size):
        if size is None:
            return "Unknown"
        elif size < 1024:
            return f"{size} B"
        elif size < 1024**2:
            return f"{size / 1024:.2f} KB"
        elif size < 1024**3:
            return f"{size / 1024**2:.2f} MB"
        else:
            return f"{size / 1024**3:.2f} GB"

    # Download options.
    # When not in a playlist, %(playlist)s becomes "NA"
    ydl_opts = {
        "format": "bv+ba/b",  # Download best video and best audio
        "merge_output_format": "mp4",  # Merge into MP4
        "outtmpl": os.path.join(download_path, "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"),
        "noplaylist": False,  # Allow playlist downloading
        "retries": 10,
        "fragment_retries": 10,
        "continue": True,
        "ignoreerrors": True,
        "progress_hooks": [progress_hook],
        "postprocessors": [
            {
                "key": "FFmpegMerger",  # Merges audio and video
            }
        ],
        "ffmpeg_location": "./ffmpeg/bin"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # After download, if the folder is named "NA", rename it.
        target_folder = download_path  # default: files are in download_path if no playlist folder
        na_folder = os.path.join(download_path, "NA")
        if os.path.exists(na_folder):
            new_folder = os.path.join(download_path, "Youtube Download")
            os.rename(na_folder, new_folder)
            target_folder = new_folder
            st.write(f"Renamed folder 'NA' to 'Youtube Download'")
        
        # Gather all downloaded MP4 files from target_folder recursively
        downloaded_files = []
        for root, dirs, files in os.walk(target_folder):
            for file in files:
                if file.endswith(".mp4"):
                    downloaded_files.append(os.path.join(root, file))
        
        if downloaded_files:
            st.write("Download finished. Click below to download your files:")
            for file_path in downloaded_files:
                with open(file_path, "rb") as f:
                    file_data = f.read()
                st.download_button(
                    label=f"Download {os.path.basename(file_path)}",
                    data=file_data,
                    file_name=os.path.basename(file_path),
                    mime="video/mp4"
                )
        else:
            st.write("No MP4 files found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit UI
def main():
    st.title("📺 YouTube Video/Playlist Downloader For Students:🎓")
    st.info("NOTE: Works For Laptop/Pc Only")

    playlist_url = st.text_input("🔗Enter YouTube Playlist URL:")
    resolution = st.selectbox("🎥Select Resolution:", ["360", "480", "720", "1080"], index=3)
    download_path = st.text_input("📂Enter download path:", value=os.getcwd())

    # Initialize progress components
    st.session_state.progress_bar = st.progress(0)
    st.session_state.progress_text = st.empty()
    st.session_state.speed_text = st.empty()
    st.session_state.size_text = st.empty()

    if st.button("Download"):
        if playlist_url and download_path:
            if not os.path.exists(download_path):
                os.makedirs(download_path)
                st.write(f"Created the directory: {download_path}")
            st.write(f"Downloading Video/Playlist from: {playlist_url} at {resolution}p to {download_path}")
            download_playlist(playlist_url, resolution, download_path)
        else:
            st.error("Please enter a valid Playlist URL and Download Path.")

    st.sidebar.subheader("👨🏻‍💻Developed By👨🏻‍💻")
    st.sidebar.subheader("⚡JASHWANTH RAJ J.R")
    st.sidebar.subheader("📚EDUCATIONAL PURPOSE ONLY🖋️")
    st.sidebar.subheader("⚠️Disclaimer:")
    st.sidebar.info(
        "1. Copyright Compliance: Use for educational/personal use only.\n"
        "2. Responsibility: The developer is not responsible for any content downloaded.\n"
        "3. Content Ownership: Intended for publicly available videos.\n"
        "4. No Liability: Use at your own risk.\n"
        "5. Terms of Service: Comply with the terms of any platform you download from."
    )

if __name__ == "__main__":
    main()
