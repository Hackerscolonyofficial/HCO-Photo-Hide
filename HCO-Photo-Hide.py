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
        <title>HCO Photo Hide</title>
        <style>
            body { 
                background-color: #0d0d0d; 
                color: #00ff99; 
                font-family: monospace; 
                text-align: center; 
                padding: 20px;
            }
            h1 { 
                color: #ff0000; 
                font-size: 2.5em; 
                margin-bottom: 20px; 
                text-shadow: 0 0 10px #ff0000;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border: 2px solid #00ff99;
                border-radius: 10px;
                background-color: #1a1a1a;
            }
            input, button, textarea { 
                padding: 12px 20px; 
                margin: 15px; 
                border-radius: 8px; 
                border: 2px solid #00ff99; 
                font-size: 1em; 
                background-color: #1a1a1a; 
                color: #00ff99; 
                outline: none;
                width: 80%;
                box-sizing: border-box;
            }
            button { 
                border: 2px solid #ff0000; 
                color: #ff0000; 
                cursor: pointer;
                transition: all 0.3s;
            }
            button:hover {
                background-color: #ff0000;
                color: #1a1a1a;
            }
            textarea {
                height: 100px;
                resize: none;
            }
            .result {
                margin: 20px;
                padding: 15px;
                border: 1px solid #00ff99;
                border-radius: 8px;
                background-color: #0d0d0d;
                word-break: break-all;
            }
            .hidden {
                display: none;
            }
            .tab {
                overflow: hidden;
                border: 1px solid #00ff99;
                background-color: #1a1a1a;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .tab button {
                background-color: inherit;
                float: left;
                border: none;
                outline: none;
                cursor: pointer;
                padding: 14px 16px;
                transition: 0.3s;
                width: 50%;
            }
            .tab button:hover {
                background-color: #00ff99;
                color: #0d0d0d;
            }
            .tab button.active {
                background-color: #00ff99;
                color: #0d0d0d;
            }
            .tabcontent {
                display: none;
                padding: 6px 12px;
                border-top: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>HCO Photo Hide</h1>
            
            <div class="tab">
                <button class="tablinks active" onclick="openTab(event, 'HideTab')">Hide Photo</button>
                <button class="tablinks" onclick="openTab(event, 'ViewTab')">View Photo</button>
            </div>
            
            <div id="HideTab" class="tabcontent" style="display: block;">
                <p>Select an image and set a password to generate a secure code</p>
                <input type="file" id="imageInput" accept="image/*" required>
                <input type="password" id="passwordInput" placeholder="Enter password" required>
                <button onclick="generateCode()">Generate Code</button>
                
                <div id="codeResult" class="result hidden">
                    <p>Your secure code:</p>
                    <textarea id="generatedCode" readonly></textarea>
                    <p>Share this code with others. They'll need to enter the password to view the image.</p>
                </div>
            </div>
            
            <div id="ViewTab" class="tabcontent">
                <p>Paste the code below to view the hidden image</p>
                <textarea id="viewCodeInput" placeholder="Paste code here"></textarea>
                <input type="password" id="viewPasswordInput" placeholder="Enter password" required>
                <button onclick="viewImage()">View Image</button>
                
                <div id="imageResult" class="result hidden">
                    <img id="hiddenImage" style="max-width: 100%; border: 2px solid #00ff99; border-radius: 8px;">
                </div>
            </div>
        </div>

        <script>
            function openTab(evt, tabName) {
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName("tabcontent");
                for (i = 0; i < tabcontent.length; i++) {
                    tabcontent[i].style.display = "none";
                }
                tablinks = document.getElementsByClassName("tablinks");
                for (i = 0; i < tablinks.length; i++) {
                    tablinks[i].className = tablinks[i].className.replace(" active", "");
                }
                document.getElementById(tabName).style.display = "block";
                evt.currentTarget.className += " active";
            }
            
            function generateCode() {
                const fileInput = document.getElementById('imageInput');
                const passwordInput = document.getElementById('passwordInput');
                
                if (!fileInput.files[0]) {
                    alert('Please select an image first');
                    return;
                }
                
                if (!passwordInput.value) {
                    alert('Please enter a password');
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    const imageData = e.target.result;
                    
                    // Create a data object to store
                    const data = {
                        image: imageData,
                        password: passwordInput.value
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
                            document.getElementById('generatedCode').value = code;
                            document.getElementById('codeResult').classList.remove('hidden');
                            
                            // Create a shareable URL
                            const url = window.location.origin + '/view.html?code=' + encodeURIComponent(code);
                            document.getElementById('generatedCode').value = url;
                        } else {
                            alert('Error: ' + data.message);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('An error occurred');
                    });
                };
                reader.readAsDataURL(fileInput.files[0]);
            }
            
            function viewImage() {
                const codeInput = document.getElementById('viewCodeInput');
                const passwordInput = document.getElementById('viewPasswordInput');
                
                if (!codeInput.value) {
                    alert('Please enter a code');
                    return;
                }
                
                if (!passwordInput.value) {
                    alert('Please enter the password');
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
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred');
                });
            }
            
            // Check if URL has a code parameter for viewing
            window.onload = function() {
                const urlParams = new URLSearchParams(window.location.search);
                const code = urlParams.get('code');
                if (code) {
                    document.getElementById('viewCodeInput').value = code;
                    // Switch to view tab
                    document.querySelector('.tablinks').click();
                    openTab(event, 'ViewTab');
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
        <title>View Hidden Image - HCO Photo Hide</title>
        <style>
            body { 
                background-color: #0d0d0d; 
                color: #00ff99; 
                font-family: monospace; 
                text-align: center; 
                padding: 50px 20px;
            }
            h1 { 
                color: #ff0000; 
                margin-bottom: 30px; 
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border: 2px solid #00ff99;
                border-radius: 10px;
                background-color: #1a1a1a;
            }
            input, button { 
                padding: 12px 20px; 
                margin: 15px; 
                border-radius: 8px; 
                border: 2px solid #00ff99; 
                font-size: 1em; 
                background-color: #1a1a1a; 
                color: #00ff99; 
                outline: none;
                width: 80%;
            }
            button { 
                border: 2px solid #ff0000; 
                color: #ff0000; 
                cursor: pointer;
            }
            #hiddenImage {
                max-width: 100%;
                margin-top: 20px;
                border: 2px solid #00ff99;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>HCO Photo Hide</h1>
            <p>Enter the password to view the hidden image</p>
            <input type="password" id="passwordInput" placeholder="Enter password" required>
            <button onclick="viewImage()">View Image</button>
            
            <div id="imageResult" style="display: none;">
                <img id="hiddenImage">
            </div>
        </div>

        <script>
            function getCodeFromURL() {
                const urlParams = new URLSearchParams(window.location.search);
                return urlParams.get('code');
            }
            
            function viewImage() {
                const passwordInput = document.getElementById('passwordInput');
                const code = getCodeFromURL();
                
                if (!passwordInput.value) {
                    alert('Please enter the password');
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
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred');
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
                'password': data['password']
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
