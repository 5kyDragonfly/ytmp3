import streamlit as st
import requests
import os
import time
import tkinter as tk
from tkinter import filedialog

# Set a default save folder (e.g., Desktop).
# You can decide later whether/how to use this on the client side.
if 'save_folder' not in st.session_state:
    st.session_state['save_folder'] = os.path.join(os.path.expanduser("~"), "Desktop")

def send_download_request(youtube_urls, save_folder):
    """
    Sends the given YouTube URLs to a server API for processing.
    Right now, it simply does a POST request and prints the response.
    Adapt this function to handle file downloads or other logic as needed.
    """
    try:
        # Replace this with your actual server endpoint
        server_url = "http://localhost:5000/download"

        payload = {
            "urls": youtube_urls,
            "save_folder": save_folder
        }

        # POST request to the server
        response = requests.post(server_url, json=payload)

        # Check the response status
        if response.status_code == 200:
            st.write("✅ Server responded successfully!")
            st.json(response.json())  # Show JSON response
        else:
            st.error(f"❌ Server Error: {response.text} (HTTP {response.status_code})")

    except Exception as e:
        st.error(f"❌ Exception: {e}")

# --- Streamlit UI ---
st.title("YouTube to MP3 Converter (API-based)")

# Allow user to select a folder using tkinter
st.write("**Save Folder:**")

def select_folder():
    root = tk.Tk()
    root.attributes('-topmost', True)  # Bring dialog to the front
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        st.session_state['save_folder'] = folder_selected

if st.button("Choose Folder"):
    select_folder()

st.write("Save Folder:", st.session_state['save_folder'])

# Let the user enter one or more YouTube URLs
links = st.text_area("Enter YouTube URLs (one per line)")
urls = [url.strip() for url in links.split('\n') if url.strip()]

# Trigger the API request when user clicks "Download MP3s"
if st.button("Download MP3s"):
    if urls:
        with st.spinner("Sending URLs to server..."):
            send_download_request(urls, st.session_state['save_folder'])
        st.success("✅ Done sending request!")
    else:
        st.warning("Please enter at least one valid YouTube URL.")
