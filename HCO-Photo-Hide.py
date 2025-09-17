import os
import time
import subprocess
from colorama import Fore, init
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import base64
import json
import re
import urllib.parse
from uuid import uuid4
from datetime import datetime

init(autoreset=True)

PORT = 8000
WORKDIR = "/data/data/com.termux/files/home/HCO-Photo-Hide"
DATA_FILE = os.path.join(WORKDIR, "data.json")

# Ensure working directory exists
os.makedirs(WORKDIR, exist_ok=True)

# --- Step 1: Tool Lock Message ---
def tool_lock():
    print(Fore.RED + "This tool is locked 🔒")
    print(Fore.YELLOW + "To unlock 🔐, you will be redirected to YouTube in 10 seconds")
    for i in range(10, 0, -1):
        print(Fore.CYAN + f"Redirecting in {i} seconds... ", end="\r")
        time.sleep(1)
    print("\n")

# --- Step 2: Open YouTube App ---
def open_youtube_app():
    subprocess.run([
        'am', 'start', '-a', 'android.intent.action.VIEW',
        '-d', 'https://youtube.com/@hackers_colony_tech'
    ])

# --- Step 3: Wait for user to return ---
def wait_for_enter():
    input(Fore.GREEN + "\nPress Enter after returning from YouTube...")

# --- Data Management ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# --- Step 4: Create HTML pages ---
def create_html():
    # Main page
    html_content = """
    <html>
    <head>
        <title>HCO Photo Hide by Azhar</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            :root {
                --primary: #00ff99;
                --secondary: #ff0066;
                --dark: #0d0d0d;
                --darker: #080808;
                --light: #1a1a1a;
                --lighter: #252525;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body { 
                background-color: var(--dark); 
                color: var(--primary); 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6;
                padding: 0;
                margin: 0;
                min-height: 100vh;
                background-image: 
                    radial-gradient(circle at 10% 20%, rgba(255, 0, 102, 0.05) 0%, transparent 20%),
                    radial-gradient(circle at 90% 80%, rgba(0, 255, 153, 0.05) 0%, transparent 20%);
            }
            
            .app-container {
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                padding: 20px 0;
                margin-bottom: 30px;
                border-bottom: 1px solid var(--lighter);
                position: relative;
            }
            
            .logo {
                font-size: 2.8rem;
                font-weight: bold;
                margin-bottom: 10px;
                background: linear-gradient(45deg, var(--primary), var(--secondary));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 15px rgba(0, 255, 153, 0.3);
                letter-spacing: 1px;
            }
            
            .tagline {
                color: #aaa;
                font-size: 1rem;
                margin-bottom: 5px;
            }
            
            .author {
                color: var(--secondary);
                font-size: 0.9rem;
                font-style: italic;
            }
            
            .dashboard {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 30px;
            }
            
            @media (max-width: 768px) {
                .dashboard {
                    grid-template-columns: 1fr;
                }
            }
            
            .card {
                background: var(--light);
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
                border: 1px solid var(--lighter);
                transition: transform 0.3s, box-shadow 0.3s;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
            }
            
            .card-header {
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 1px solid var(--lighter);
                display: flex;
                align-items: center;
            }
            
            .card-icon {
                font-size: 1.5rem;
                margin-right: 10px;
                color: var(--secondary);
            }
            
            .card-title {
                font-size: 1.4rem;
                font-weight: 600;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
                color: #ccc;
            }
            
            input, textarea, button { 
                padding: 14px 16px; 
                margin: 8px 0; 
                border-radius: 8px; 
                border: 1px solid var(--lighter); 
                font-size: 1rem; 
                background-color: var(--darker); 
                color: var(--primary); 
                outline: none;
                width: 100%;
                transition: all 0.3s;
            }
            
            input:focus, textarea:focus {
                border-color: var(--primary);
                box-shadow: 0 0 0 2px rgba(0, 255, 153, 0.2);
            }
            
            button { 
                background: linear-gradient(45deg, var(--secondary), #ff0066cc);
                color: white; 
                cursor: pointer;
                border: none;
                font-weight: 600;
                letter-spacing: 0.5px;
                margin-top: 10px;
            }
            
            button:hover {
                background: linear-gradient(45deg, #ff0066cc, var(--secondary));
                box-shadow: 0 0 15px rgba(255, 0, 102, 0.4);
            }
            
            .btn-secondary {
                background: linear-gradient(45deg, var(--lighter), #252525cc);
            }
            
            .btn-secondary:hover {
                background: linear-gradient(45deg, #252525cc, var(--lighter));
                box-shadow: 0 0 15px rgba(0, 255, 153, 0.2);
            }
            
            textarea {
                height: 100px;
                resize: none;
                font-family: monospace;
            }
            
            .result {
                margin: 20px 0;
                padding: 20px;
                border: 1px solid var(--lighter);
                border-radius: 8px;
                background-color: var(--darker);
                word-break: break-all;
            }
            
            .result-title {
                font-weight: 600;
                margin-bottom: 10px;
                color: var(--secondary);
            }
            
            .hidden {
                display: none;
            }
            
            .image-preview {
                max-width: 100%;
                border-radius: 8px;
                border: 1px solid var(--lighter);
                margin-top: 15px;
            }
            
            .footer {
                text-align: center;
                padding: 20px 0;
                margin-top: 40px;
                border-top: 1px solid var(--lighter);
                color: #666;
                font-size: 0.9rem;
            }
            
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 8px;
                background: var(--light);
                border-left: 4px solid var(--secondary);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                transform: translateX(100%);
                transition: transform 0.3s;
                z-index: 1000;
            }
            
            .notification.show {
                transform: translateX(0);
            }
            
            .notification.success {
                border-left-color: var(--primary);
            }
            
            .notification.error {
                border-left-color: var(--secondary);
            }
            
            .hint {
                font-size: 0.85rem;
                color: #777;
                margin-top: 5px;
            }
            
            .instructions {
                background: var(--darker);
                padding: 20px;
                border-radius: 8px;
                margin-top: 30px;
                border: 1px solid var(--lighter);
            }
            
            .instructions h3 {
                margin-bottom: 15px;
                color: var(--secondary);
            }
            
            .instructions ol {
                padding-left: 20px;
            }
            
            .instructions li {
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="header">
                <div class="logo">HCO Photo Hide</div>
                <div class="tagline">Secure Image Sharing with Password Protection</div>
                <div class="author">by Azhar - Hackers Colony</div>
            </div>
            
            <div class="dashboard">
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">🔒</div>
                        <div class="card-title">Hide Photo</div>
                    </div>
                    <p>Select an image and set a password to generate a secure code</p>
                    
                    <div class="form-group">
                        <label for="imageInput">Select Image:</label>
                        <input type="file" id="imageInput" accept="image/*" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="passwordInput">Set Password:</label>
                        <input type="password" id="passwordInput" placeholder="Enter a strong password" required>
                        <div class="hint">Remember this password - it's required to view the image</div>
                    </div>
                    
                    <button onclick="generateCode()">Generate Secure Code</button>
                    
                    <div id="codeResult" class="result hidden">
                        <div class="result-title">Your Secure Sharing Code:</div>
                        <textarea id="generatedCode" readonly></textarea>
                        <button class="btn-secondary" onclick="copyToClipboard()">Copy to Clipboard</button>
                        <div class="hint">Share this code with others. They'll need the password to view the image.</div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">🔍</div>
                        <div class="card-title">View Photo</div>
                    </div>
                    <p>Paste the code below to view the hidden image</p>
                    
                    <div class="form-group">
                        <label for="viewCodeInput">Paste Code:</label>
                        <textarea id="viewCodeInput" placeholder="Paste the secure code here"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="viewPasswordInput">Enter Password:</label>
                        <input type="password" id="viewPasswordInput" placeholder="Enter the password" required>
                    </div>
                    
                    <button onclick="viewImage()">View Hidden Image</button>
                    
                    <div id="imageResult" class="result hidden">
                        <div class="result-title">Hidden Image:</div>
                        <img id="hiddenImage" class="image-preview">
                    </div>
                </div>
            </div>
            
            <div class="instructions">
                <h3>How to Use HCO Photo Hide:</h3>
                <ol>
                    <li><strong>Hide Photo:</strong> Select an image, set a password, and generate a secure code</li>
                    <li><strong>Share:</strong> Send the code and password to your recipient through different channels for security</li>
                    <li><strong>View:</strong> Recipient pastes the code, enters the password, and views the image</li>
                    <li><strong>Security:</strong> The image is stored locally and accessible only with the correct password</li>
                </ol>
            </div>
            
            <div class="footer">
                HCO Photo Hide by Azhar © 2023 | Hackers Colony Tech
            </div>
        </div>

        <div id="notification" class="notification hidden"></div>

        <script>
            function showNotification(message, type = 'success') {
                const notification = document.getElementById('notification');
                notification.textContent = message;
                notification.className = 'notification ' + type;
                notification.classList.add('show');
                
                setTimeout(() => {
                    notification.classList.remove('show');
                }, 3000);
            }
            
            function generateCode() {
                const fileInput = document.getElementById('imageInput');
                const passwordInput = document.getElementById('passwordInput');
                
                if (!fileInput.files[0]) {
                    showNotification('Please select an image first', 'error');
                    return;
                }
                
                if (!passwordInput.value) {
                    showNotification('Please enter a password', 'error');
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    const imageData = e.target.result;
                    
                    // Create a data object to store
                    const data = {
                        image: imageData,
                        password: passwordInput.value,
                        timestamp: new Date().toISOString()
                    };
                    
                    // Send to server
                    fetch('/save', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            const code = data.code;
                            const url = window.location.origin + '/view.html?code=' + encodeURIComponent(code);
                            document.getElementById('generatedCode').value = url;
                            document.getElementById('codeResult').classList.remove('hidden');
                            showNotification('Secure code generated successfully!');
                        } else {
                            showNotification('Error: ' + data.message, 'error');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showNotification('An error occurred', 'error');
                    });
                };
                reader.readAsDataURL(fileInput.files[0]);
            }
            
            function viewImage() {
                const codeInput = document.getElementById('viewCodeInput');
                const passwordInput = document.getElementById('viewPasswordInput');
                
                if (!codeInput.value) {
                    showNotification('Please enter a code', 'error');
                    return;
                }
                
                if (!passwordInput.value) {
                    showNotification('Please enter the password', 'error');
                    return;
                }
                
                // Extract code from URL if needed
                let code = codeInput.value;
                if (code.includes('/view.html?code=')) {
                    const urlParams = new URLSearchParams(code.split('?')[1]);
                    code = urlParams.get('code');
                }
                
                // Send to server
                fetch('/view', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        code: code,
                        password: passwordInput.value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('hiddenImage').src = data.image;
                        document.getElementById('imageResult').classList.remove('hidden');
                        showNotification('Image unlocked successfully!');
                    } else {
                        showNotification('Error: ' + data.message, 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showNotification('An error occurred', 'error');
                });
            }
            
            function copyToClipboard() {
                const textarea = document.getElementById('generatedCode');
                textarea.select();
                document.execCommand('copy');
                showNotification('Code copied to clipboard!');
            }
            
            // Check if URL has a code parameter for viewing
            window.onload = function() {
                const urlParams = new URLSearchParams(window.location.search);
                const code = urlParams.get('code');
                if (code) {
                    document.getElementById('viewCodeInput').value = code;
                    document.getElementById('viewPasswordInput').focus();
                }
            };
        </script>
    </body>
    </html>
    """
    
    with open(os.path.join(WORKDIR, "index.html"), "w") as f:
        f.write(html_content)
    
    # View page for direct access via shared URL
    view_html = """
    <html>
    <head>
        <title>View Hidden Image - HCO Photo Hide by Azhar</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            :root {
                --primary: #00ff99;
                --secondary: #ff0066;
                --dark: #0d0d0d;
                --darker: #080808;
                --light: #1a1a1a;
                --lighter: #252525;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body { 
                background-color: var(--dark); 
                color: var(--primary); 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6;
                padding: 0;
                margin: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-image: 
                    radial-gradient(circle at 10% 20%, rgba(255, 0, 102, 0.05) 0%, transparent 20%),
                    radial-gradient(circle at 90% 80%, rgba(0, 255, 153, 0.05) 0%, transparent 20%);
            }
            
            .container {
                max-width: 500px;
                width: 90%;
                padding: 30px;
                border: 1px solid var(--lighter);
                border-radius: 12px;
                background-color: var(--light);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                text-align: center;
            }
            
            .logo {
                font-size: 2.2rem;
                font-weight: bold;
                margin-bottom: 15px;
                background: linear-gradient(45deg, var(--primary), var(--secondary));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 15px rgba(0, 255, 153, 0.3);
            }
            
            .tagline {
                color: #aaa;
                font-size: 1rem;
                margin-bottom: 25px;
            }
            
            .author {
                color: var(--secondary);
                font-size: 0.9rem;
                margin-bottom: 30px;
                font-style: italic;
            }
            
            .form-group {
                margin-bottom: 20px;
                text-align: left;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
                color: #ccc;
            }
            
            input, button { 
                padding: 14px 16px; 
                margin: 8px 0; 
                border-radius: 8px; 
                border: 1px solid var(--lighter); 
                font-size: 1rem; 
                background-color: var(--darker); 
                color: var(--primary); 
                outline: none;
                width: 100%;
                transition: all 0.3s;
            }
            
            input:focus {
                border-color: var(--primary);
                box-shadow: 0 0 0 2px rgba(0, 255, 153, 0.2);
            }
            
            button { 
                background: linear-gradient(45deg, var(--secondary), #ff0066cc);
                color: white; 
                cursor: pointer;
                border: none;
                font-weight: 600;
                letter-spacing: 0.5px;
                margin-top: 10px;
            }
            
            button:hover {
                background: linear-gradient(45deg, #ff0066cc, var(--secondary));
                box-shadow: 0 0 15px rgba(255, 0, 102, 0.4);
            }
            
            #hiddenImage {
                max-width: 100%;
                margin-top: 20px;
                border: 1px solid var(--lighter);
                border-radius: 8px;
            }
            
            .footer {
                text-align: center;
                margin-top: 30px;
                color: #666;
                font-size: 0.9rem;
            }
            
            .notification {
                padding: 15px 20px;
                border-radius: 8px;
                background: var(--light);
                border-left: 4px solid var(--secondary);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                margin-bottom: 20px;
                display: none;
            }
            
            .notification.show {
                display: block;
            }
            
            .notification.success {
                border-left-color: var(--primary);
            }
            
            .notification.error {
                border-left-color: var(--secondary);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">HCO Photo Hide</div>
            <div class="tagline">Secure Image Sharing</div>
            <div class="author">by Azhar - Hackers Colony</div>
            
            <div id="notification" class="notification hidden"></div>
            
            <div id="passwordForm">
                <div class="form-group">
                    <label for="passwordInput">Enter Password to View Image:</label>
                    <input type="password" id="passwordInput" placeholder="Enter the password" required autofocus>
                </div>
                
                <button onclick="viewImage()">View Hidden Image</button>
            </div>
            
            <div id="imageResult" style="display: none;">
                <img id="hiddenImage">
            </div>
        </div>

        <div class="footer">
            HCO Photo Hide by Azhar © 2023
        </div>

        <script>
            function getCodeFromURL() {
                const urlParams = new URLSearchParams(window.location.search);
                return urlParams.get('code');
            }
            
            function showNotification(message, type = 'success') {
                const notification = document.getElementById('notification');
                notification.textContent = message;
                notification.className = 'notification ' + type;
                notification.classList.add('show');
                
                setTimeout(() => {
                    notification.classList.remove('show');
                }, 3000);
            }
            
            function viewImage() {
                const passwordInput = document.getElementById('passwordInput');
                const code = getCodeFromURL();
                
                if (!passwordInput.value) {
                    showNotification('Please enter the password', 'error');
                    return;
                }
                
                fetch('/view', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        code: code,
                        password: passwordInput.value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('hiddenImage').src = data.image;
                        document.getElementById('imageResult').style.display = 'block';
                        document.getElementById('passwordForm').style.display = 'none';
                        showNotification('Image unlocked successfully!');
                    } else {
                        showNotification('Error: ' + data.message, 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showNotification('An error occurred', 'error');
                });
            }
            
            // Focus on password input when page loads
            window.onload = function() {
                document.getElementById('passwordInput').focus();
            };
        </script>
    </body>
    </html>
    """
    
    with open(os.path.join(WORKDIR, "view.html"), "w") as f:
        f.write(view_html)

# --- Step 5: Custom HTTP Request Handler ---
class HCORequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WORKDIR, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path.startswith('/view.html'):
            # Serve the view page for direct access
            self.path = '/view.html'
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/save':
            # Handle image saving
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Generate a unique code
            code = str(uuid4())
            
            # Load existing data
            all_data = load_data()
            
            # Store the image and password
            all_data[code] = {
                'image': data['image'],
                'password': data['password'],
                'timestamp': data.get('timestamp', datetime.now().isoformat())
            }
            
            # Save the data
            save_data(all_data)
            
            # Return the code to the client
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'success': True,
                'code': code
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/view':
            # Handle image viewing
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Load existing data
            all_data = load_data()
            
            # Check if code exists
            if data['code'] in all_data:
                stored_data = all_data[data['code']]
                
                # Check password
                if data['password'] == stored_data['password']:
                    # Return the image
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        'success': True,
                        'image': stored_data['image']
                    }
                    self.wfile.write(json.dumps(response).encode())
                else:
                    # Wrong password
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        'success': False,
                        'message': 'Incorrect password'
                    }
                    self.wfile.write(json.dumps(response).encode())
            else:
                # Code not found
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'success': False,
                    'message': 'Invalid code'
                }
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404, "Not Found")

# --- Step 6: Start HTTP Server ---
def start_server():
    os.chdir(WORKDIR)
    server = HTTPServer(('0.0.0.0', PORT), HCORequestHandler)
    print(Fore.GREEN + f"Server started at http://localhost:{PORT}")
    server.serve_forever()

# --- Main Execution ---
if __name__ == "__main__":
    # Show tool lock message
    tool_lock()
    
    # Open YouTube app
    open_youtube_app()
    
    # Wait for user to return
    wait_for_enter()
    
    # Create HTML pages
    create_html()
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Get local IP address
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        network_url = f"http://{local_ip}:{PORT}"
        print(Fore.GREEN + f"Network access: {network_url}")
    except:
        network_url = f"http://localhost:{PORT}"
        print(Fore.YELLOW + "Could not determine network IP, using localhost")
    
    # Open browser to the local server
    subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', f'http://localhost:{PORT}'])
    
    print(Fore.CYAN + "HCO Photo Hide is now running!")
    print(Fore.CYAN + "Share this URL with others on the same network:")
    print(Fore.CYAN + network_url)
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\nServer stopped by user")
