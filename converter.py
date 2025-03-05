# server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.json or {}
    urls = data.get("urls", [])
    save_folder = data.get("save_folder", "not_provided")

    print("Received URLs:", urls)
    print("Save folder:", save_folder)
    
    # Just return some example response for now.
    return jsonify({
        "message": "Received your data!",
        "count": len(urls),
        "save_folder": save_folder
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
