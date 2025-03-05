# server.py
from flask import Flask, request, send_file
import io
import zipfile
import json

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.json or {}
    urls = data.get("urls", [])
    save_folder = data.get("save_folder", "not_provided")

    print("Received URLs:", urls)
    print("Save folder:", save_folder)
    
    # --- Here you would do the actual downloading/conversion. ---
    # For a hollow example, let's create a small in-memory zip with
    # a single text file to mimic a "download".
    
    memory_zip = io.BytesIO()
    with zipfile.ZipFile(memory_zip, mode='w') as z:
        z.writestr("README.txt", "This is a dummy file. Replace with your MP3(s).")
    memory_zip.seek(0)

    return send_file(
        memory_zip,
        download_name='converted_files.zip',
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
