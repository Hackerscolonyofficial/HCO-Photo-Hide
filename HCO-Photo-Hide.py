import os
import time
import subprocess
from colorama import Fore, init
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import base64
import json
import re

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

# --- Step 4: Create HTML page with download feature ---
def create_html():
    html_content = f"""
    <html>
    <head>
        <title>HCO Photo Hide</title>
        <style>
            body {{ background-color: #0d0d0d; color: #00ff99; font-family: monospace; text-align: center; padding-top: 50px; }}
            h1 {{ color: #ff0000; font-size: 2.5em; margin-bottom: 20px; }}
            input, button {{ padding: 12px 20px; margin: 15px; border-radius: 8px; border: 2px solid #00ff99; font-size: 1em; background-color: #1a1a1a; color:#00ff99; outline:none; }}
            button {{ border:2px solid #ff0000; color:#ff0000; }}
        </style>
    </head>
    <body>
        <h1>HCO Photo Hide by Azhar</h1>
        <input type="file" id="photo" /><br/>
        <input type="password" placeholder="Enter Password" id="password" /><br/>
        <button onclick="generateCode()">Generate Code</button>
        <p id="msg" style="color:#00ffff;font-weight:bold;"></p>
        <script>
            function generateCode() {{
                let fileInput = document.getElementById('photo');
                let password = document.getElementById('password').value;
                if(fileInput.files.length==0) {{ alert("Select a photo!"); return; }}
                if(password=="") {{ alert("Enter a password!"); return; }}
                let reader = new FileReader();
                reader.onload = function() {{
                    let data = reader.result.split(',')[1];
                    fetch('/save', {{
                        method:'POST',
                        headers:{{'Content-Type':'application/json'}},
                        body: JSON.stringify({{photo:data, password:password, name:fileInput.files[0].name}})
                    }}).then(r=>r.text()).then(t=>{{
                        document.getElementById('msg').innerText=t;

                        // Download .hco file
                        let blob = new Blob([btoa(data + password)], {{type: 'text/plain'}});
                        let link = document.createElement('a');
                        link.href = URL.createObjectURL(blob);
                        link.download = fileInput.files[0].name.split('.')[0] + ".hco";
                        link.click();
                    }});
                }}
                reader.readAsDataURL(fileInput.files[0]);
            }}
        </script>
    </body>
    </html>
    """
    os.makedirs(WORKDIR, exist_ok=True)
    with open(os.path.join(WORKDIR, "index.html"), "w") as f:
        f.write(html_content)

# --- Step 5: HTTP server ---
class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            encrypted = base64.b64encode((data['photo'] + data['password']).encode()).decode()
            save_path = os.path.join(WORKDIR, "hidden_" + data['name'] + ".txt")
            with open(save_path, "w") as f:
                f.write(encrypted)
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Photo Hidden Successfully!")
        else:
            super().do_GET()

def start_server():
    os.chdir(WORKDIR)
    server = HTTPServer(("127.0.0.1", PORT), MyHandler)
    server.serve_forever()

# --- Step 6: Start Cloudflare Tunnel and open public URL ---
def start_tunnel_and_open():
    proc = subprocess.Popen(
        ['cloudflared', 'tunnel', '--url', f'http://127.0.0.1:{PORT}'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    public_url = None
    while True:
        line = proc.stdout.readline()
        if line:
            match = re.search(r'https://[^\s]+', line)
            if match:
                public_url = match.group(0)
                break

    print(Fore.GREEN + f"\n[✔] Public URL: {public_url}")
    subprocess.run([
        'am', 'start', '-a', 'android.intent.action.VIEW',
        '-d', public_url
    ])
    print(Fore.GREEN + "\nHCO Photo Hide is now live on any phone!")

# --- Main ---
def main():
    os.system("clear")
    tool_lock()
    open_youtube_app()
    wait_for_enter()
    create_html()

    threading.Thread(target=start_server, daemon=True).start()
    start_tunnel_and_open()

if __name__ == "__main__":
    main()
