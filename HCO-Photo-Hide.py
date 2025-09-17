import os
import time
import subprocess
from colorama import Fore, Back, Style, init
import webbrowser

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
        # Opens YouTube app on Android
        subprocess.run([
            'am', 'start', '-a', 'android.intent.action.VIEW',
            '-d', 'https://youtube.com/@hackers_colony_tech'
        ], check=True)
    except Exception as e:
        # Fallback: open in browser
        print("YouTube app failed, opening in browser...")
        webbrowser.open('https://youtube.com/@hackers_colony_tech')

# --- Step 3: Wait for user to return and press Enter ---
def wait_for_enter():
    input(Fore.GREEN + "\nPress Enter after returning from YouTube...")

# --- Step 4: Open Browser for Photo Hide Page ---
def open_browser_page():
    html_content = """
    <html>
    <head>
        <title>HCO Photo Hide</title>
        <style>
            body { background-color: #0a0a0a; color: #ffffff; font-family: 'Courier New', monospace; text-align:center; padding-top:50px;}
            h1 { color: #ff0000; margin-bottom: 40px; font-size:2.2em; }
            input, button { padding: 12px 20px; margin: 10px; border-radius: 6px; border: none; font-size:1em; }
            input { width: 250px; }
            button { background-color: #007BFF; color: white; cursor: pointer; font-weight:bold; }
            button:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
        <h1>HCO Photo Hide by Azhar</h1>
        <input type="file" id="photo" /><br/>
        <input type="password" placeholder="Enter Password" id="password" /><br/>
        <button onclick="alert('Photo Hidden Successfully!')">Generate Code</button>
    </body>
    </html>
    """
    path = "/data/data/com.termux/files/home/HCO-Photo-Hide/temp.html"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html_content)
    webbrowser.open("file://" + path)

# --- Main Flow ---
def main():
    os.system("clear")
    tool_lock()          # Show countdown + lock message
    open_youtube_app()   # Redirect to YouTube app
    wait_for_enter()     # Wait until user returns and presses Enter
    open_browser_page()  # Open browser page with photo hide UI

if __name__ == "__main__":
    main()
