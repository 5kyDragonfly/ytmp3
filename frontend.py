import streamlit as st
import requests
import os

# By convention, let's default to the user's "Downloads" folder locally
if 'save_folder' not in st.session_state:
    st.session_state['save_folder'] = os.path.join(os.path.expanduser("~"), "Downloads")

def send_download_request(youtube_urls):
    """
    Sends the given YouTube URLs to a server API for processing.
    Expects the server to return file data (e.g. MP3 or ZIP) as bytes.
    """
    try:
        # Replace this with your actual server endpoint
        server_url = "https://285f-2001-4451-43c2-5d00-e80b-628c-c50f-f71b.ngrok-free.app/download"

        payload = {
            "urls": youtube_urls,
            # You can pass this along if your server needs it, or ignore.
            "save_folder": st.session_state['save_folder']
        }

        response = requests.post(server_url, json=payload)

        # Check the response status
        if response.status_code == 200:
            return response
        else:
            st.error(f"❌ Server Error: {response.text} (HTTP {response.status_code})")
            return None

    except Exception as e:
        st.error(f"❌ Exception: {e}")
        return None

# --- Streamlit UI ---
st.title("YouTube to MP3 Converter by Sky")

# Display the default "save" folder (which is basically for reference).
st.write("**Downloads Folder (for reference):**", st.session_state['save_folder'])

# Let the user enter one or more YouTube URLs
links = st.text_area("Enter YouTube URLs (one per line)")
urls = [url.strip() for url in links.split('\n') if url.strip()]

# Trigger the API request when user clicks "Convert and Download"
if st.button("Convert and Download"):
    if urls:
        with st.spinner("Contacting server for conversion..."):
            response = send_download_request(urls)
            if response:
                # The server might return a ZIP or a single MP3 file, etc.
                # For demonstration, let's assume it returns a zip file's bytes:
                zip_data = response.content

                # Provide a download button for the user to save the file
                st.download_button(
                    label="Download Converted Files",
                    data=zip_data,
                    file_name="converted_files.zip",
                    mime="application/zip"
                )

                st.success("✅ Conversion complete! Click above to download.")
    else:
        st.warning("Please enter at least one valid YouTube URL.")
