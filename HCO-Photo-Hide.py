#!/usr/bin/env python3
# HCO-Photo-Hide.py
# GitHub-ready Termux tool with countdown, unlock redirect, and browser generator.
# Code by Azhar

import os, time, shutil, webbrowser

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except Exception:
    class _C: 
        def __getattr__(self, k): return ''
    Fore = Style = _C()

YOUTUBE = "https://youtube.com/@hackers_colony_tech?si=pvdCWZggTIuGb0ya"
OUT_HTML = "hco-photo-hide-generator.html"

HTML_CONTENT = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>HCO-Photo-Hide</title>
<style>
body{font-family:Arial,Helvetica,sans-serif;background:#0f1724;color:#fff;margin:0;padding:20px}
.app{max-width:800px;margin:auto;background:#1e293b;padding:20px;border-radius:12px}
h1{margin:0 0 10px 0}
.lead{color:#9ca3af;margin:0 0 20px 0}
.blue-box{display:none;background:#1d4ed8;padding:14px;border-radius:8px;margin-top:20px;text-align:center}
.blue-box span{color:#ff1c1c;font-weight:bold;font-size:20px}
.modal-backdrop{position:fixed;inset:0;background:rgba(0,0,0,0.8);display:flex;align-items:center;justify-content:center;z-index:9999}
.modal{background:#1e293b;padding:20px;border-radius:10px;max-width:400px;text-align:center}
.countdown-big{font-size:40px;font-weight:bold;margin:10px 0}
button{background:#06b6d4;border:none;padding:10px 18px;border-radius:8px;font-weight:bold;cursor:pointer}
</style>
</head>
<body>
<div class="app">
  <h1>HCO-Photo-Hide — Generator</h1>
  <p class="lead">Choose your photo, add optional password & countdown, then generate a single HTML file to send.</p>

  <input id="file" type="file" accept="image/*"><br><br>
  <input id="password" type="password" placeholder="Password (optional)"><br><br>
  <input id="countdown" type="number" min="0" value="5"> seconds countdown<br><br>
  <button id="generate">Generate .html</button>

  <div id="afterReturn" class="blue-box"><span>HCO Photo Hide</span></div>
</div>

<div id="modalRoot" class="modal-backdrop">
  <div class="modal">
    <h2>Tool Locked</h2>
    <p>This tool is not free. It will unlock after visiting YouTube.</p>
    <div class="countdown-big" id="toolCountdown">10</div>
    <p>Opening YouTube in <span id="cdText">10</span> sec…</p>
    <button id="openNow">Open Now</button>
  </div>
</div>

<script>
const YOUTUBE = "%YOUTUBE%";
let sec=10; const cdEl=document.getElementById('toolCountdown'); const cdText=document.getElementById('cdText');
function startCD(){const t=setInterval(()=>{sec--;cdEl.textContent=sec;cdText.textContent=sec;if(sec<=0){clearInterval(t);openYT();}},1000);}
function openYT(){window.open(YOUTUBE,"_blank");document.getElementById('modalRoot').style.display='none';alert("YouTube opened. After returning, press Enter to continue.");}
document.getElementById('openNow').onclick=openYT; startCD();
window.addEventListener('keydown',(e)=>{if(e.key==='Enter'){document.getElementById('afterReturn').style.display='block';}});
</script>
</body></html>"""

def write_html(path):
    with open(path,"w",encoding="utf-8") as f:
        f.write(HTML_CONTENT.replace("%YOUTUBE%", YOUTUBE))

def open_file(path):
    abs_path = os.path.abspath(path)
    if shutil.which("termux-open"): os.system(f'termux-open "{abs_path}"'); return
    if shutil.which("am"): os.system(f'am start -a android.intent.action.VIEW -d "file://{abs_path}"'); return
    webbrowser.open("file://"+abs_path)

def main():
    print(Fore.CYAN+"[+] Generating HCO-Photo-Hide browser tool...")
    time.sleep(2)
    write_html(OUT_HTML)
    print(Fore.GREEN+"[+] File created: "+OUT_HTML)
    print(Fore.YELLOW+"[+] Opening in browser...")
    time.sleep(2)
    open_file(OUT_HTML)
    print(Fore.MAGENTA+"[✓] Done! Use the browser to select photo & generate recipient HTML.")

if __name__=="__main__":
    main()
