import os
import time
import subprocess
from colorama import Fore, init

init(autoreset=True)

# --- Step 1: Tool Lock Message with Countdown ---
def tool_lock():
    print(Fore.RED + "This tool is locked 🔒")
    print(Fore.YELLOW + "To unlock 🔐, you will be redirected to YouTube in 10 seconds")
    for i in range(10, 0, -1):
        print(Fore.CYAN + f"Redirecting in {i} seconds... ", end="\r")
        time.sleep(1)
    print("\n")

# --- Step 2: Open YouTube App ---
def open_youtube_app():
    try:
        subprocess.run([
            'am', 'start', '-a', 'android.intent.action.VIEW',
            '-d', 'https://youtube.com/@hackers_colony_tech'
        ], check=True)
    except:
        subprocess.run([
            'am', 'start', '-a', 'android.intent.action.VIEW',
            '-d', 'https://youtube.com/@hackers_colony_tech'
        ])

# --- Step 3: Wait for user to return ---
def wait_for_enter():
    input(Fore.GREEN + "\nPress Enter after returning from YouTube...")

# --- Step 4: Open hacker-style browser page ---
def open_browser_page():
    html_content = """
    <html>
    <head>
        <title>HCO Photo Hide</title>
        <style>
            @keyframes glitch {
                0% { text-shadow: 2px 0 red, -2px 0 cyan; }
                20% { text-shadow: -2px 0 red, 2px 0 cyan; }
                40% { text-shadow: 2px 2px red, -2px -2px cyan; }
                60% { text-shadow: -2px -2px red, 2px 2px cyan; }
                80% { text-shadow: 2px -2px red, -2px 2px cyan; }
                100% { text-shadow: 0 0 red, 0 0 cyan; }
            }
            body {
                background-color: #0d0d0d;
                color: #00ff99;
                font-family: 'Courier New', monospace;
                text-align: center;
                padding-top: 50px;
            }
            h1 {
                color: #ff0000;
                font-size: 2.5em;
                animation: glitch 1s infinite;
                margin-bottom: 40px;
            }
            .countdown {
                font-size: 1.5em;
                color: #00ffff;
                margin-bottom: 20px;
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
                box-shadow: 0 0 10px #00ff99;
            }
            input:hover, button:hover {
                box-shadow: 0 0 15px #00ff99, 0 0 20px #00ff99;
            }
            button {
                cursor: pointer;
                font-weight: bold;
                border: 2px solid #ff0000;
                color: #ff0000;
                text-shadow: 0 0 3px #ff0000;
            }
            button:hover {
                box-shadow: 0 0 15px #ff0000, 0 0 25px #ff0000;
            }
        </style>
    </head>
    <body>
        <h1>HCO Photo Hide by Azhar</h1>
        <div class="countdown" id="countdown">Countdown: 10</div>
        <input type="file" id="photo" /><br/>
        <input type="password" placeholder="Enter Password" id="password" /><br/>
        <button onclick="alert('Photo Hidden Successfully!')">Generate Code</button>
        <script>
            let count = 10;
            let countdownEl = document.getElementById('countdown');
            let interval = setInterval(() => {
                countdownEl.innerText = "Countdown: " + count;
                count--;
                if(count < 0) clearInterval(interval);
            }, 1000);
        </script>
    </body>
    </html>
    """
    path = "/data/data/com.termux/files/home/HCO-Photo-Hide/temp.html"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html_content)

    # Force Android browser to open HTML
    subprocess.run([
        'am', 'start', '-a', 'android.intent.action.VIEW',
        '-d', f'file://{path}',
        '-t', 'text/html'
    ])

# --- Main Flow ---
def main():
    os.system("clear")
    tool_lock()
    open_youtube_app()
    wait_for_enter()
    open_browser_page()

if __name__ == "__main__":
    main()
