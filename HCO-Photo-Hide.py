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
        <p>Select an image to hide or reveal data</p>
        
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" required>
            <br>
            <input type="text" name="secret" placeholder="Secret data to hide (optional)">
            <br>
            <button type="submit" name="action" value="hide">Hide Data in Image</button>
            <button type="submit" name="action" value="reveal">Reveal Data from Image</button>
        </form>
        
        <div id="result" style="margin-top: 30px;"></div>
        
        <script>
            document.querySelector('form').addEventListener('submit', function(e) {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = '<p>Processing your request...</p>';
            });
        </script>
    </body>
    </html>
    """
    
    with open(os.path.join(WORKDIR, "index.html"), "w") as f:
        f.write(html_content)
    
    # Success page
    success_html = """
    <html>
    <head>
        <title>Success - HCO Photo Hide</title>
        <style>
            body { background-color: #0d0d0d; color: #00ff99; font-family: monospace; text-align: center; padding-top: 50px; }
            h1 { color: #00ff00; }
            a { color: #ff9900; text-decoration: none; margin: 10px; display: inline-block; padding: 10px; border: 1px solid #ff9900; }
        </style>
    </head>
    <body>
        <h1>Operation Successful!</h1>
        <p>{{MESSAGE}}</p>
        <a href="/">Back to Home</a>
        <a href="/download/{{FILENAME}}">Download File</a>
    </body>
    </html>
    """
    
    with open(os.path.join(WORKDIR, "success.html"), "w") as f:
        f.write(success_html)

# --- Step 5: Custom HTTP Request Handler ---
class HCORequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WORKDIR, **kwargs)
    
    def do_GET(self):
        if self.path.startswith('/download/'):
            filename = self.path.split('/')[-1]
            filepath = os.path.join(WORKDIR, filename)
            
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.end_headers()
                
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/upload':
            content_type = self.headers['Content-Type']
            if not content_type.startswith('multipart/form-data'):
                self.send_error(400, "Bad Request: expecting multipart/form-data")
                return
            
            # Parse form data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse multipart form data (simplified)
            parts = content_type.split("boundary=")
            if len(parts) < 2:
                self.send_error(400, "Bad Request: no boundary")
                return
            
            boundary = parts[1].encode()
            parts = post_data.split(boundary)
            
            file_data = None
            secret_data = ""
            action = ""
            
            for part in parts:
                if b'name="image"' in part and b'filename="' in part:
                    # Extract file data
                    file_start = part.find(b'\r\n\r\n') + 4
                    file_end = part.rfind(b'\r\n')
                    file_data = part[file_start:file_end]
                    
                    # Extract filename
                    filename_match = re.search(b'filename="([^"]+)"', part)
                    if filename_match:
                        filename = filename_match.group(1).decode()
                
                if b'name="secret"' in part:
                    # Extract secret data
                    data_start = part.find(b'\r\n\r\n') + 4
                    data_end = part.rfind(b'\r\n')
                    secret_data = part[data_start:data_end].decode()
                
                if b'name="action"' in part:
                    # Extract action
                    data_start = part.find(b'\r\n\r\n') + 4
                    data_end = part.rfind(b'\r\n')
                    action = part[data_start:data_end].decode()
            
            if not file_data:
                self.send_error(400, "Bad Request: no file uploaded")
                return
            
            # Process the request
            if action == "hide":
                # Hide data in image
                output_filename = f"hidden_{filename}"
                output_path = os.path.join(WORKDIR, output_filename)
                
                # Write the original file
                with open(output_path, 'wb') as f:
                    f.write(file_data)
                
                # Append the secret data to the end of the file (simplified steganography)
                with open(output_path, 'ab') as f:
                    if secret_data:
                        f.write(b"\nHCO_STEGANOGRAPHY_START\n")
                        f.write(base64.b64encode(secret_data.encode()))
                        f.write(b"\nHCO_STEGANOGRAPHY_END\n")
                
                # Show success page
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                with open(os.path.join(WORKDIR, "success.html"), "r") as f:
                    success_content = f.read()
                
                success_content = success_content.replace("{{MESSAGE}}", f"Data hidden in {output_filename}")
                success_content = success_content.replace("{{FILENAME}}", output_filename)
                self.wfile.write(success_content.encode())
                
            elif action == "reveal":
                # Reveal data from image
                temp_path = os.path.join(WORKDIR, f"temp_{filename}")
                with open(temp_path, 'wb') as f:
                    f.write(file_data)
                
                # Read the file to extract hidden data
                with open(temp_path, 'rb') as f:
                    content = f.read()
                
                # Look for the hidden data markers
                start_marker = b"\nHCO_STEGANOGRAPHY_START\n"
                end_marker = b"\nHCO_STEGANOGRAPHY_END\n"
                
                start_idx = content.find(start_marker)
                end_idx = content.find(end_marker)
                
                if start_idx != -1 and end_idx != -1:
                    # Extract and decode the hidden data
                    encoded_data = content[start_idx + len(start_marker):end_idx]
                    secret_data = base64.b64decode(encoded_data).decode()
                    
                    # Show success page with revealed data
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    with open(os.path.join(WORKDIR, "success.html"), "r") as f:
                        success_content = f.read()
                    
                    success_content = success_content.replace("{{MESSAGE}}", f"Hidden data revealed: {secret_data}")
                    success_content = success_content.replace("{{FILENAME}}", "")  # No file to download
                    self.wfile.write(success_content.encode())
                else:
                    self.send_error(400, "No hidden data found in this image")
                
                # Clean up temp file
                os.remove(temp_path)
            
            else:
                self.send_error(400, "Bad Request: invalid action")

# --- Step 6: Start HTTP Server ---
def start_server():
    os.chdir(WORKDIR)
    server = HTTPServer(('localhost', PORT), HCORequestHandler)
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
    
    # Open browser to the local server
    subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', f'http://localhost:{PORT}'])
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\nServer stopped by user")
