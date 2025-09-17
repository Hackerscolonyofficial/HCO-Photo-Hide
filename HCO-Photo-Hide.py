#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, time, webbrowser
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

# YouTube channel link
YOUTUBE_LINK = "https://youtube.com/@hackers_colony_tech?si=pvdCWZggTIuGb0ya"

# Countdown function
def countdown(msg, seconds=8):
    for i in range(seconds,0,-1):
        print(Fore.YELLOW + f"{msg} {i}")
        time.sleep(1)

# Clear screen function
def clear():
    os.system('clear' if os.name=='posix' else 'cls')

# Tool lock message
def tool_lock():
    clear()
    print(Fore.RED + Style.BRIGHT + "\nThis tool is locked 🔒")
    print(Fore.CYAN + "To unlock 🔐 the tool you will be redirected to YouTube")
    print(Fore.CYAN + "Subscribe & click the bell 🔔\n")
    countdown("Redirecting in", 8)
    print(Fore.GREEN + "Opening YouTube...")
    time.sleep(1)
    # Open YouTube app (works in Termux)
    webbrowser.open(YOUTUBE_LINK)
    input(Fore.MAGENTA + "\nPress Enter after subscribing to continue...")

# Main HCO Photo Hide tool
def main_tool():
    clear()
    # Display final header
    print(Fore.WHITE + Style.BRIGHT + Back.BLUE + "\n   HCO Photo Hide by Azhar   \n" + Style.RESET_ALL)
    print(Fore.GREEN + "\nSelect a photo and set a password to generate the hidden photo HTML.\n")

    # Ask for photo path
    photo_path = input(Fore.CYAN + "Enter path to image: ").strip()
    if not os.path.isfile(photo_path):
        print(Fore.RED + "File not found! Exiting...")
        sys.exit(1)

    password = input(Fore.CYAN + "Enter password to protect the photo: ").strip()
    if not password:
        print(Fore.RED + "Password cannot be empty! Exiting...")
        sys.exit(1)

    # Read image and encode to base64
    import base64
    with open(photo_path,"rb") as f:
        img_data = f.read()
    img_b64 = base64.b64encode(img_data).decode('utf-8')

    # Generate HTML content
    html_content = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HCO Photo Hide</title>
<style>
body{{background:#111;color:#2bff6b;font-family:monospace;text-align:center;padding:20px;}}
h1{{color:red;}}
#theimg{{display:none;max-width:90vw;max-height:80vh;border:3px solid #2bff6b;border-radius:6px;}}
#water{{color:red;font-weight:bold;margin-top:10px;}}
#count{{font-size:4rem;}}
</style>
</head>
<body>
<h1>HCO Photo Hide</h1>
<div id="count">8</div>
<img id="theimg" src="data:image/png;base64,{img_b64}">
<div id="water">HCO Photo Hide by Azhar</div>
<script>
const STORED="{base64.b64encode(password.encode()).decode()}";
function safeB64(s){return btoa(s);}
setTimeout(()=>{
    let p = prompt('Enter password to reveal photo:');
    if(btoa(p)!==STORED){alert('Wrong password'); return;}
    let n=8; const cnt=document.getElementById('count'); const img=document.getElementById('theimg');
    const interval=setInterval(()=>{
        cnt.textContent=n; n--;
        if(n<0){clearInterval(interval);cnt.style.display='none';img.style.display='block';}},800);
},200);
</script>
</body>
</html>"""

    # Save generated HTML
    output_file = "HCO-Photo-Hide.html"
    with open(output_file,"w") as f:
        f.write(html_content)
    print(Fore.GREEN + f"\n✅ Generated HTML saved as {output_file}")

if __name__=="__main__":
    tool_lock()
    main_tool()
