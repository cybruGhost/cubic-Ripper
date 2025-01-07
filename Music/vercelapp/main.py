from flask import Flask, render_template, request, redirect, url_for, flash
import os
import re
import yt_dlp
from urllib.error import HTTPError

app = Flask(__name__)

# Set the main folder (current working directory) and cubic_downloads folder
MAIN_FOLDER = os.getcwd()  # Current working directory
DOWNLOAD_FOLDER = os.path.join(MAIN_FOLDER, "cubic_downloads")

# Ensure the cubic_downloads directory exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

app.secret_key = 'your_secret_key'  # For flash messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def handle_video_link():
    video_link = request.form['video_link'].strip()
    if video_link.lower() == "exit":
        flash("Goodbye!", "info")
        return redirect(url_for('index'))
    
    check_video_link(video_link)
    return redirect(url_for('index'))

def check_video_link(url: str):
    """Validate the provided YouTube link and identify its type."""
    if re.search(r"youtube\.com/watch\?", url) or re.search(r"youtu\.be", url):
        download_video(url)
    elif re.search(r"youtube\.com/playlist\?", url):
        download_playlist(url)
    else:
        flash("The URL you entered is invalid. Please try again.", "danger")

def download_video(video_link: str):
    """Download a single YouTube video as MP3 using yt_dlp."""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',  # Best audio quality
            'extractaudio': True,  # Extract audio
            'audioformat': 'mp3',  # Set audio format to MP3
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # Set output path to cubic_downloads
            'noplaylist': True,  # Disable playlist download
            'quiet': False,  # Show progress
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_link, download=True)
            video_title = info_dict.get('title', 'Video')
            flash(f"Downloading '{video_title}'...", "info")
            flash(f"Success! '{video_title}' has been downloaded as MP3.", "success")

    except Exception as e:
        flash(f"An error occurred while downloading the video: {e}", "danger")

def download_playlist(video_link: str):
    """Download all videos in a YouTube playlist as MP3 using yt_dlp."""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',  # Best audio quality
            'extractaudio': True,  # Extract audio
            'audioformat': 'mp3',  # Set audio format to MP3
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # Set output path to cubic_downloads
            'noplaylist': False,  # Enable playlist download
            'quiet': False,  # Show progress
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(video_link, download=True)
            playlist_title = playlist_info.get('title', 'Playlist')
            flash(f"Fetching playlist: {playlist_title}", "info")
            flash("Playlist download completed!", "success")

    except Exception as e:
        flash(f"An error occurred with the playlist: {e}", "danger")

if __name__ == "__main__":
    app.run(debug=True)

