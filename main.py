import os
import bcrypt
import requests as r
from flask import Flask, jsonify, render_template, session, redirect, request, send_from_directory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask Config
app = Flask(__name__, static_folder="static")
app.secret_key = os.urandom(24)

# Create the downloads folder if it doesn't exist
SAVE_FOLDER = "downloads"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Load credentials
USERNAME = os.getenv("username")
PASSWORD_HASH = os.getenv("password_hash").encode() if os.getenv("password_hash") else None


# Route to list files
@app.route('/api/files', methods=['GET'])
def list_files():
    if not session.get('logged_in'):
        return redirect('/login')

    files = os.listdir(SAVE_FOLDER)
    return jsonify({"files": files})


@app.route('/api/login', methods=['POST'])
def api_login():
    if session.get('logged_in'):
        return jsonify({"success": True, "message": "Already logged in!"}), 200

    data = request.get_json()
    username_input = data.get('username')
    password = data.get('password')

    if not username_input or not password:
        return jsonify({"error": "Missing Username or Password"}), 400

    if username_input == USERNAME and bcrypt.checkpw(password.encode(), PASSWORD_HASH):
        session['logged_in'] = True
        return jsonify({"success": True, "message": "Login successful"}), 200

    print("❌ Password Check Failed!")
    return jsonify({"error": "Invalid Username or Password"}), 401


@app.route('/api/downloads/start-download', methods=['POST'])
def start_download():
    if not session.get('logged_in'):
        return jsonify({"error": "You must be logged in to do this action!"}), 401

    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "Missing required parameters!"}), 400

    filename = os.path.join(SAVE_FOLDER, os.path.basename(url))

    response = r.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return jsonify({"success": f"Saved {filename} to server!"}), 200
    else:
        return jsonify({"error": "Failed to download file!"}), 500


@app.route('/api/download/from_server', methods=['GET'])
def download_from_server():
    if not session.get('logged_in'):
        return jsonify({"error": "You must be logged in to do this action!"}), 401

    filename = request.args.get('filename')  # Use request.args.get() for GET requests

    if not filename:
        return jsonify({"error": "Missing required parameters!"}), 400

    file_path = os.path.join(SAVE_FOLDER, filename)
    if os.path.exists(file_path):
        return send_from_directory(SAVE_FOLDER, filename)
    else:
        return jsonify({"error": "File not found on server! Please try to re-download it!"}), 404
@app.route('/')
def index():
    return redirect('/dashboard' if session.get('logged_in') else '/login')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('dashboard.html')

@app.route('/login')
def login():
    if session.get('logged_in'):
        return redirect('/dashboard')
    return render_template('login.html')

if __name__ == "__main__":
    app.run(port=8236, host='0.0.0.0')
