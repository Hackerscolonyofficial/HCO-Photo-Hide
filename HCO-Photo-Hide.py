import os
import time
import subprocess
from colorama import Fore, init
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import base64

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

# --- Step 4: Create HTML page ---
def create_html():
    html_content = f"""
    <html>
    <head>
        <title>HCO Photo Hide</title>
        <style>
            @keyframes glitch {{
                0% {{ text-shadow: 2px 0 red, -2px 0 cyan; }}
                20% {{ text-shadow: -2px 0 red, 2px 0 cyan; }}
                40% {{ text-shadow: 2px 2px red, -2px -2px cyan; }}
                60% {{ text-shadow: -2px -2px red, 2px 2px cyan; }}
                80% {{ text-shadow: 2px -2px red, -2px 2px cyan; }}
                100% {{ text-shadow: 0 0 red, 0 0 cyan; }}
            }}
            body {{
                background-color: #0d0d0d;
                color: #00ff99;
                font-family: 'Courier New', monospace;
                text-align: center;
                padding-top: 50px;
            }}
            h1 {{
                color: #ff0000;
                font-size: 2.5em;
                animation: glitch 1s infinite;
                margin-bottom: 20px;
            }}
            .countdown {{ font-size: 1.5em; color:#00ffff; margin-bottom:30px; }}
            input, button {{
                padding: 12px 20px;
                margin: 15px;
                border-radius: 8px;
                border: 2px solid #00ff99;
                font-size: 1em;
                background-color: #1a1a1a;
                color:#00ff99;
                outline:none;
                box-shadow:0 0 10px #00ff99;
            }}
            input:hover, button:hover {{ box-shadow:0 0 15px #00ff99,0 0 20px #00ff99; }}
            button {{
                cursor:pointer;
                font-weight:bold;
                border:2px solid #ff0000;
                color:#ff0000;
                text-shadow:0 0 3px #ff0000;
            }}
            button:hover {{ box-shadow:0 0 15px #ff0000,0 0 25px #ff0000; }}
        </style>
    </head>
    <body>
        <h1>HCO Photo Hide by Azhar</h1>
        <div class="countdown" id="countdown">Countdown: 10</div>
        <input type="file" id="photo" /><br/>
        <input type="password" placeholder="Enter Password" id="password" /><br/>
        <button onclick="generateCode()">Generate Code</button>
        <p id="msg" style="color:#00ffff;font-weight:bold;"></p>
        <script>
            let count = 10;
            let countdownEl = document.getElementById('countdown');
            let interval = setInterval(() => {{
                countdownEl.innerText = "Countdown: " + count;
                count--;
                if(count < 0) clearInterval(interval);
            }}, 1000);

            function generateCode() {{
                let fileInput = document.getElementById('photo');
                let password = document.getElementById('password').value;
                if(fileInput.files.length==0) {{
                    alert("Select a photo first!");
                    return;
                }}
                if(password=="") {{
                    alert("Enter a password!");
                    return;
                }}
                let reader = new FileReader();
                reader.onload = function() {{
                    let data = reader.result.split(',')[1]; // base64
                    fetch('/save', {{
                        method:'POST',
                        headers:{{'Content-Type':'application/json'}},
                        body: JSON.stringify({{photo:data, password:password, name:fileInput.files[0].name}})
                    }}).then(r=>r.text()).then(t=>document.getElementById('msg').innerText=t);
                }}
                reader.readAsDataURL(fileInput.files[0]);
            }}
        </script>
    </body>
    </html>
    """
    path = os.path.join(WORKDIR, "index.html")
    os.makedirs(WORKDIR, exist_ok=True)
    with open(path, "w") as f:
        f.write(html_content)

# --- Step 5: HTTP server with save handler ---
class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            import json
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
    server = HTTPServer(("0.0.0.0", PORT), MyHandler)
    server.serve_forever()

def open_browser():
    url = f"http://127.0.0.1:{PORT}/index.html"
    subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', url])

# --- Main Flow ---
def main():
    os.system("clear")
    tool_lock()
    open_youtube_app()
    wait_for_enter()
    create_html()
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    open_browser()
    print(Fore.GREEN + "\nBrowser opened. Photo Hide ready!")

if __name__ == "__main__":
    main()
