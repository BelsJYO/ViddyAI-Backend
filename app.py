from flask import Flask, request, jsonify
import requests
import os
import subprocess
import threading
import time

app = Flask(__name__)

# Start the FastAPI server in a separate thread
def start_fastapi():
    subprocess.run(["python", "main.py"])

# Start FastAPI server
fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
fastapi_thread.start()

# Give FastAPI time to start
time.sleep(2)

@app.route('/')
def index():
    return jsonify({"message": "AI Video Editor Flask Wrapper", "version": "1.0.0"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_to_fastapi(path):
    # Proxy requests to FastAPI server
    fastapi_url = f"http://localhost:8000/api/{path}"
    
    if request.method == 'GET':
        response = requests.get(fastapi_url, params=request.args)
    elif request.method == 'POST':
        response = requests.post(fastapi_url, json=request.get_json(), params=request.args)
    elif request.method == 'PUT':
        response = requests.put(fastapi_url, json=request.get_json(), params=request.args)
    elif request.method == 'DELETE':
        response = requests.delete(fastapi_url, params=request.args)
    
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

