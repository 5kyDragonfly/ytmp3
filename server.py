# server.py
from flask import Flask, request, send_file
import yt_dlp
import tempfile
import zipfile
import os
import io

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.json or {}
    urls = data.get("urls", [])
    save_folder = data.get("save_folder", "not_provided")

    print("Received URLs:", urls)
    print("Save folder (for reference):", save_folder)
    
    if not urls:
        return {"error": "No URLs received"}, 400

    # 1. Create a temp directory to store the downloaded MP3 files.
    with tempfile.TemporaryDirectory() as temp_dir:
        # 2. Download/convert each URL into the temp directory.
        for url in urls:
            try:
                ydl_opts = {
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192"
                    }],
                    "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
                    "noplaylist": True,
                    "quiet": True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                print(f"Error downloading {url}: {e}")

        # 3. Zip all MP3 files in that temp directory into an in-memory buffer.
        memory_zip = io.BytesIO()
        with zipfile.ZipFile(memory_zip, mode='w') as zf:
            for filename in os.listdir(temp_dir):
                if filename.lower().endswith(".mp3"):
                    file_path = os.path.join(temp_dir, filename)
                    # Write the MP3 file into the zip
                    zf.write(file_path, arcname=filename)

        # 4. Reset the buffer pointer to the beginning.
        memory_zip.seek(0)

        # 5. Send the zip back to the client.
        return send_file(
            memory_zip,
            download_name='converted_files.zip',  # Flask 2.x uses download_name
            as_attachment=True
        )

if __name__ == '__main__':
    # Make sure you have ffmpeg installed, and this environment has yt_dlp
    # e.g. pip install flask yt_dlp
    app.run(host='0.0.0.0', port=5000, debug=True)
