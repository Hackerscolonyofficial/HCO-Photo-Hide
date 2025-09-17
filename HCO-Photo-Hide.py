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

init(autoreset=True)

PORT = 8000
WORKDIR = "/data/data/com.termux/files/home/HCO-Photo-Hide"

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

# --- Step 4: Create HTML pages ---
def create_html():
    os.makedirs(WORKDIR, exist_ok=True)
    
    # Main page
    html_content = """
    <html>
    <head>
        <title>HCO Photo Hide</title>
        <style>
            body { background-color: #0d0d0d; color: #00ff99; font-family: monospace; text-align: center; padding-top: 50px; }
            h1 { color: #ff0000; font-size: 2.5em; margin-bottom: 20px; }
            input, button { padding: 12px 20px; margin: 15px; border-radius: 8px; border: 2px solid #00ff99; font-size: 1em; background-color: #1a1a1a; color:#00ff99; outline:none; }
            button { border:2px solid #ff0000; color:#ff0000; }
        </style>
    </head>
    <body>
        <h1>HCO Photo Hide by Azhar</h1>
        <input type="file" id="photo" /><br/>
        <input type="password" placeholder="Enter Password" id="password" /><br/>
        <button onclick="generateCode()">Generate Code</button>
        <p id="msg" style="color:#00ffff;font-weight:bold;"></p>
        <script>
            function generateCode() {
                let fileInput = document.getElementById('photo');
                let password = document.getElementById('password').value;
                if(fileInput.files.length==0) { alert("Select a photo!"); return; }
                if(password=="") { alert("Enter a password!"); return; }
                let reader = new FileReader();
                reader.onload = function() {
                    let data = reader.result.split(',')[1];
                    fetch('/save', {
                        method:'POST',
                        headers:{'Content-Type':'application/json'},
                        body: JSON.stringify({photo:data, password:password, name:fileInput.files[0].name})
                    }).then(r=>r.text()).then(t=>{
                        document.getElementById('msg').innerText = "Code: " + t;
                        // Create a shareable link
                        let shareLink = window.location.origin + '/view?code=' + encodeURIComponent(t);
                        document.getElementById('msg').innerHTML += "<br><br>Share this link:<br><input type='text' value='" + shareLink + "' style='width: 80%; padding: 10px;' readonly>";
                    });
                }
                reader.readAsDataURL(fileInput.files[0]);
            }
        </script>
    </body>
    </html>
    """
    
    with open(os.path.join(WORKDIR, "index.html"), "w") as f:
        f.write(html_content)
    
    # Viewer page
    viewer_content = """
    <html>
    <head>
        <title>View Hidden Photo</title>
        <style>
            body { background-color: #0d0d0d; color: #00ff99; font-family: monospace; text-align: center; padding-top: 50px; }
            h1 { color: #ff0000; font-size: 2.5em; margin-bottom: 20px; }
            input, button { padding: 12px 20px; margin: 15px; border-radius: 8px; border: 2px solid #00ff99; font-size: 1em; background-color: #1a1a1a; color:#00ff99; outline:none; }
            button { border:2px solid #ff0000; color:#ff0000; }
            img { max-width: 90%; margin-top: 20px; border: 2px solid #00ff99; }
        </style>
    </head>
    <body>
        <h1>View Hidden Photo</h1>
        <input type="password" placeholder="Enter Password" id="password" /><br/>
        <button onclick="viewPhoto()">View Photo</button>
        <div id="result"></div>
        <script>
            function getQueryParam(name) {
                const urlParams = new URLSearchParams(window.location.search);
                return urlParams.get(name);
            }
            
            function viewPhoto() {
                let password = document.getElementById('password').value;
                if(password=="") { alert("Enter a password!"); return; }
                
                let code = getQueryParam('code');
                if(!code) {
                    document.getElementById('result').innerHTML = "<p style='color:red'>No code provided!</p>";
                    return;
                }
                
                fetch('/decode?code=' + encodeURIComponent(code) + '&password=' + encodeURIComponent(password))
                    .then(response => response.json())
                    .then(data => {
                        if(data.success) {
                            document.getElementById('result').innerHTML = "<img src='data:image/jpeg;base64," + data.photo + "' alt='Hidden Photo' />";
                        } else {
                            document.getElementById('result').innerHTML = "<p style='color:red'>" + data.message + "</p>";
                        }
                    })
                    .catch(error => {
                        document.getElementById('result').innerHTML = "<p style='color:red'>Error: " + error + "</p>";
                    });
            }
        </script>
    </body>
    </html>
    """
    
    with open(os.path.join(WORKDIR, "viewer.html"), "w") as f:
        f.write(viewer_content)

# --- Step 5: HTTP server ---
class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WORKDIR, **kwargs)
    
    def do_GET(self):
        if self.path.startswith('/view'):
            self.path = '/viewer.html'
        elif self.path.startswith('/decode'):
            # Handle decoding request
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            code = query_params.get('code', [''])[0]
            password = query_params.get('password', [''])[0]
            
            try:
                # Decode the base64 string
                decoded = base64.b64decode(code).decode('utf-8')
                
                # The last part should be the password
                if decoded.endswith(password):
                    # Extract the image data (everything except the password)
                    photo_data = decoded[:-len(password)]
                    
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "success": True,
                        "photo": photo_data
                    }).encode())
                else:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "success": False,
                        "message": "Incorrect password!"
                    }).encode())
            except Exception as e:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": False,
                    "message": f"Error decoding: {str(e)}"
                }).encode())
            return
            
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            # Combine photo data and password, then encode
            combined = data['photo'] + data['password']
            encrypted = base64.b64encode(combined.encode()).decode()
            
            # Generate a simple filename
            filename = f"hidden_{int(time.time())}.txt"
            save_path = os.path.join(WORKDIR, filename)
            
            with open(save_path, "w") as f:
                f.write(encrypted)
            
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(encrypted.encode())
        else:
            self.send_error(404)

def start_server():
    os.chdir(WORKDIR)
    server = HTTPServer(("127.0.0.1", PORT), MyHandler)
    print(Fore.GREEN + f"[+] Server started on port {PORT}")
    server.serve_forever()

# --- Step 6: Start Cloudflare Tunnel and open public URL ---
def start_tunnel_and_open():
    # Run tunnel in background
    proc = subprocess.Popen(
        ['cloudflared', 'tunnel', '--url', f'http://127.0.0.1:{PORT}'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    public_url = None
    timeout = time.time() + 10  # 10 seconds timeout
    
    print(Fore.YELLOW + "[+] Starting Cloudflare tunnel...")
    
    while time.time() < timeout:
        line = proc.stderr.readline()
        if not line:
            time.sleep(0.1)
            continue
            
        match = re.search(r'https://[^\s]+\.trycloudflare\.com', line)
        if match:
            public_url = match.group(0)
            break

    if public_url:
        print(Fore.GREEN + f"[✔] Public URL: {public_url}")
        # Open browser automatically
        subprocess.run([
            'am', 'start', '-a', 'android.intent.action.VIEW',
            '-d', public_url
        ])
        print(Fore.GREEN + "\nHCO Photo Hide is now live on any phone!")
        
        # Keep the tunnel process running
        try:
            proc.wait()
        except KeyboardInterrupt:
            proc.terminate()
    else:
        print(Fore.RED + "[!] Failed to get public URL from Cloudflare tunnel")
        proc.terminate()

# --- Main ---
def main():
    os.system("clear")
    tool_lock()
    open_youtube_app()
    wait_for_enter()
    create_html()

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Give the server a moment to start
    time.sleep(1)
    
    start_tunnel_and_open()

if __name__ == "__main__":
    main()
