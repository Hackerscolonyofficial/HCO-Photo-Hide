#!/usr/bin/env python3
# HCO-Photo-Hide.py
# GitHub-ready Termux tool with Termux countdown, YouTube redirect, generator HTML and recipient HTML creation.
# Code by Azhar

import os
import sys
import time
import shutil
import webbrowser

# Color output for Termux
try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except Exception:
    class _C:
        def __getattr__(self, k): return ''
    Fore = Back = Style = _C()

YOUTUBE = "https://youtube.com/@hackers_colony_tech?si=pvdCWZggTIuGb0ya"
GEN_HTML = "hco-photo-hide-generator.html"

# Generator HTML (browser). It contains a tool-lock modal with an 8-second countdown,
# file picker, password input and generator logic (Web Crypto). The generated recipient
# HTML will be self-contained and include the same heading and reveal countdown.
GEN_HTML_TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>HCO Photo Hide by Azhar</title>
<style>
  body{font-family:Inter,Arial,Helvetica,sans-serif;background:#071026;color:#e9f0fb;margin:0;padding:20px;display:flex;justify-content:center}
  .card{max-width:900px;width:100%;background:linear-gradient(180deg,#0b1220,#071026);padding:18px;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,0.6)}
  .title-box{background:#0b3b8a;padding:10px;border-radius:8px;text-align:center;margin-bottom:12px}
  .title-box .title{color:#ff2b2b;font-weight:800;font-size:20px}
  label{display:block;color:#9fb3c8;margin-top:10px}
  input[type=text],input[type=password],input[type=number]{width:100%;padding:8px;border-radius:8px;border:1px solid rgba(255,255,255,0.04);background:transparent;color:inherit}
  input[type=file]{color:inherit}
  button{background:linear-gradient(90deg,#7c3aed,#06b6d4);border:none;padding:10px 14px;border-radius:10px;color:#041023;font-weight:700;cursor:pointer;margin-top:12px}
  .preview{height:220px;border-radius:8px;background:linear-gradient(180deg,rgba(255,255,255,0.01),transparent);display:flex;align-items:center;justify-content:center;overflow:hidden;margin-top:10px}
  img.preview-img{max-width:100%;max-height:100%;object-fit:contain}
  /* modal */
  .modal-backdrop{position:fixed;inset:0;background:rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;z-index:9999}
  .modal{background:#0f1724;padding:20px;border-radius:10px;max-width:420px;width:90%;text-align:center}
  .countdown-big{font-size:44px;font-weight:800;margin:8px 0;color:#ffcc00}
  .small{color:#9fb3c8}
</style>
</head>
<body>
  <div class="card" role="main">
    <div class="title-box"><div class="title">HCO Photo Hide by Azhar</div></div>

    <label>Choose image</label>
    <input id="file" type="file" accept="image/*" />

    <div class="preview" id="preview">No image selected</div>

    <label>Password (optional)</label>
    <input id="password" type="password" placeholder="Leave empty for no password" />

    <label>Reveal countdown (seconds)</label>
    <input id="revealCountdown" type="number" min="0" value="5" />

    <button id="generate">Generate .html</button>
  </div>

  <!-- Tool-lock modal (also forces a brief redirect to YouTube) -->
  <div id="modalRoot" class="modal-backdrop" aria-hidden="false" role="dialog">
    <div class="modal">
      <div style="font-weight:800;font-size:18px;margin-bottom:6px">Tool locked — quick check required</div>
      <div class="small">This tool is not free. We will open our YouTube channel briefly. Return and press Enter to continue.</div>
      <div class="countdown-big" id="toolCountdown">8</div>
      <div class="small" id="cdText">Opening YouTube in 8 seconds…</div>
      <div style="margin-top:12px"><button id="openNow">Open Now</button></div>
    </div>
  </div>

<script>
const YOUTUBE = "%YOUTUBE%";
let toolCount = 8;
const toolCountdownEl = document.getElementById('toolCountdown');
const cdText = document.getElementById('cdText');
const modalRoot = document.getElementById('modalRoot');
const openNow = document.getElementById('openNow');

function startToolCountdown(){
  toolCountdownEl.textContent = toolCount;
  cdText.textContent = "Opening YouTube in " + toolCount + " seconds…";
  const t = setInterval(()=>{
    toolCount--;
    toolCountdownEl.textContent = toolCount;
    cdText.textContent = "Opening YouTube in " + toolCount + " seconds…";
    if(toolCount<=0){
      clearInterval(t);
      // force navigation (this usually triggers YouTube app)
      location.href = YOUTUBE;
    }
  },1000);
}

// allow manual open
openNow.addEventListener('click', ()=>{
  location.href = YOUTUBE;
});

// when user presses Enter after returning, hide modal and reveal small blue box heading
window.addEventListener('keydown', (e)=>{
  if(e.key === 'Enter'){
    modalRoot.style.display = 'none';
    // display simple in-page confirmation (same blue header already visible in top)
    const after = document.querySelector('.title-box');
    if(after) after.style.boxShadow = '0 8px 30px rgba(11,59,138,0.35)';
  }
});

// start countdown on load
startToolCountdown();

/* ========== Generator logic (Web Crypto) ========== */
const fileInput = document.getElementById('file');
const preview = document.getElementById('preview');
const pwInput = document.getElementById('password');
const genBtn = document.getElementById('generate');
const revealInput = document.getElementById('revealCountdown');

let loadedBase64 = null;
fileInput.addEventListener('change', ()=>{
  const f = fileInput.files && fileInput.files[0];
  if(!f) return;
  const reader = new FileReader();
  reader.onload = ()=> {
    const url = reader.result;
    preview.innerHTML = '<img class="preview-img" src="'+url+'">';
    loadedBase64 = url.split(',')[1];
  };
  reader.readAsDataURL(f);
});

function toHex(buffer){
  return Array.from(new Uint8Array(buffer)).map(b=>b.toString(16).padStart(2,'0')).join('');
}
function rand(len){ const a=new Uint8Array(len); crypto.getRandomValues(a); return a.buffer; }
async function deriveKey(password, salt, iterations=200000){
  const enc = new TextEncoder();
  const baseKey = await crypto.subtle.importKey('raw', enc.encode(password), {name:'PBKDF2'}, false, ['deriveKey']);
  return crypto.subtle.deriveKey({name:'PBKDF2', salt: salt, iterations: iterations, hash:'SHA-256'}, baseKey, {name:'AES-GCM', length:256}, true, ['encrypt','decrypt']);
}

function guessMime(b64){
  if(!b64) return 'image/*';
  const header = atob(b64.slice(0,32));
  if(header.startsWith('\\xFF\\xD8')) return 'image/jpeg';
  if(header.startsWith('\\x89PNG')) return 'image/png';
  if(header.startsWith('RIFF') && header.indexOf('WEBP')>0) return 'image/webp';
  return 'image/*';
}

async function encryptImage(base64, password){
  const salt = rand(16);
  const iv = rand(12);
  const key = await deriveKey(password||'', salt);
  const binary = Uint8Array.from(atob(base64), c=>c.charCodeAt(0));
  const ct = await crypto.subtle.encrypt({name:'AES-GCM', iv:iv}, key, binary);
  return {
    cipherHex: toHex(ct),
    ivHex: toHex(iv),
    saltHex: toHex(salt),
    iterations: 200000,
    mime: guessMime(base64)
  };
}

function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

/* recipient HTML template builder */
function makeRecipientHTML(payload, title, revealSeconds){
  const tpl = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>${escapeHtml(title)}</title>
<style>
 body{font-family:Inter,Arial;background:#071026;color:#e9f0fb;margin:0;padding:20px;display:flex;justify-content:center}
 .wrap{max-width:900px;width:100%;background:#0b1220;padding:18px;border-radius:12px}
 .title-box{background:#0b3b8a;padding:10px;border-radius:8px;text-align:center;margin-bottom:12px}
 .title-box .title{color:#ff2b2b;font-weight:800;font-size:20px}
 .box{background:rgba(255,255,255,0.02);padding:12px;border-radius:10px}
 .count{font-size:40px;font-weight:800;margin:8px 0;color:#ffcc00}
 img.revealed{max-width:100%;display:block;border-radius:8px}
</style></head><body>
 <div class="wrap">
   <div class="title-box"><div class="title">${escapeHtml(title)}</div></div>
   <div class="box">
     <p>This file contains an encrypted image. Enter the password (if required) then click Reveal.</p>
     <input id="pw" type="password" placeholder="Password (if required)"/>
     <button id="reveal">Reveal</button>
     <div id="countArea" style="display:none"><div class="count" id="count">${revealSeconds}</div><div>Waiting to reveal...</div></div>
     <div id="imageArea" style="margin-top:12px;display:none;text-align:center"></div>
     <div id="err" style="color:#ff8585;margin-top:8px;display:none"></div>
   </div>
 </div>
<script>
const payload = ${JSON.stringify(payload)};
function hexToBuffer(hex){ if(hex.length%2) hex='0'+hex; const u=new Uint8Array(hex.length/2); for(let i=0;i<u.length;i++) u[i]=parseInt(hex.substr(i*2,2),16); return u.buffer; }
async function deriveKey(password,salt,iterations){ const enc=new TextEncoder(); const pk=await crypto.subtle.importKey('raw',enc.encode(password),{name:'PBKDF2'},false,['deriveKey']); return crypto.subtle.deriveKey({name:'PBKDF2',salt:salt,iterations:iterations,hash:'SHA-256'},pk,{name:'AES-GCM',length:256},true,['decrypt']); }
async function decryptAndShow(password){ document.getElementById('err').style.display='none'; try{ const salt=hexToBuffer(payload.saltHex); const iv=hexToBuffer(payload.ivHex); const ct=hexToBuffer(payload.cipherHex); const key=await deriveKey(password,salt,payload.iterations); const plain=await crypto.subtle.decrypt({name:'AES-GCM',iv:iv},key,ct); const blob=new Blob([plain],{type:payload.mime||'image/*'}); const url=URL.createObjectURL(blob); document.getElementById('imageArea').innerHTML='<img class="revealed" src="'+url+'">'; document.getElementById('imageArea').style.display='block'; }catch(e){ console.error(e); document.getElementById('err').textContent='Decryption failed — wrong password or/or corrupted file.'; document.getElementById('err').style.display='block'; } }
document.getElementById('reveal').addEventListener('click', ()=>{ const pw=document.getElementById('pw').value||''; const cd=${Number(revealSeconds)}; if(cd>0){ document.getElementById('countArea').style.display='block'; let t=cd; document.getElementById('count').textContent=t; const timer=setInterval(()=>{ t--; document.getElementById('count').textContent=t; if(t<=0){ clearInterval(timer); document.getElementById('countArea').style.display='none'; decryptAndShow(pw); } },1000); } else { decryptAndShow(pw); } });
</script>
</body></html>`;
  return tpl;
}

/* generate and download file in browser */
genBtn.addEventListener('click', async ()=>{
  if(!loadedBase64){ alert('Please choose an image first.'); return; }
  const password = pwInput.value || '';
  if(password === ''){
    if(!confirm('Password is empty — the generated file will be decryptable by anyone who opens it. Continue?')) return;
  }
  genBtn.disabled = true;
  genBtn.textContent = 'Encrypting...';
  try{
    const payload = await encryptImage(loadedBase64, password||'');
    const title = 'HCO Photo Hide by Azhar';
    const rv = Number(document.getElementById('revealCountdown').value) || 0;
    const recipient = makeRecipientHTML(payload, title, rv);
    const blob = new Blob([recipient], {type:'text/html'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const fname = 'HCO-photo-'+Date.now()+'.html';
    a.href = url; a.download = fname; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(()=>URL.revokeObjectURL(url), 5000);
    alert('Generated file downloaded: ' + fname + '\\nSend it to your recipient and share password separately.');
  }catch(e){
    console.error(e);
    alert('Error: ' + e.message);
  }finally{
    genBtn.disabled = false;
    genBtn.textContent = 'Generate .html';
  }
});
</script>
</body>
</html>
'''

def write_generator(path):
    content = GEN_HTML_TEMPLATE.replace("%YOUTUBE%", YOUTUBE)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def open_path_in_android(path):
    # try termux-open -> am -> webbrowser
    abspath = os.path.abspath(path)
    if shutil.which("termux-open"):
        os.system(f'termux-open "{abspath}"')
        return True
    if shutil.which("am"):
        # use Android intent to open file in browser (file://)
        os.system(f'am start -a android.intent.action.VIEW -d "file://{abspath}"')
        return True
    try:
        webbrowser.open("file://" + abspath)
        return True
    except Exception:
        return False

def open_youtube_android():
    # attempt to open YouTube app using am start (best on Android)
    if shutil.which("am"):
        os.system(f'am start -a android.intent.action.VIEW -d "{YOUTUBE}"')
        return True
    if shutil.which("termux-open"):
        os.system(f'termux-open "{YOUTUBE}"')
        return True
    try:
        webbrowser.open(YOUTUBE)
        return True
    except Exception:
        return False

def termux_lock_flow():
    print(Style.BRIGHT + Fore.RED + "\n[!] Tool locked — quick check required\n")
    print(Fore.WHITE + "To unlock, you'll be redirected briefly to our YouTube channel.")
    print(Fore.YELLOW + "Do NOT send password with the file. Return and press Enter to continue.\n")
    time.sleep(1)

    # colorful countdown 8->1
    for i in range(8, 0, -1):
        print(" " * 40, end="\r")  # clear line
        print(Style.BRIGHT + Fore.RED + f"Redirecting to YouTube in {i}...", end="\r")
        time.sleep(1)
    print("\n" + Fore.GREEN + "Opening YouTube now...")

    # open YouTube
    opened = open_youtube_android()
    if not opened:
        print(Fore.RED + "Could not open YouTube automatically. Open this link manually:")
        print(YOUTUBE)

    # wait for user to return and press Enter
    try:
        input(Fore.CYAN + "\nPress Enter after returning from YouTube to continue...")
    except KeyboardInterrupt:
        print("\n" + Fore.RED + "Interrupted. Exiting.")
        sys.exit(0)

    # Show blue box with red bold text (no ASCII art)
    title = "HCO Photo Hide by Azhar"
    padding = " " * 6
    width = len(title) + len(padding)*2
    # print a blue line above and below by printing spaces with blue background
    print()
    print(Back.BLUE + " " * (width))
    print(Back.BLUE + padding + Fore.RED + Style.BRIGHT + title + Style.NORMAL + Back.BLUE + padding)
    print(Back.BLUE + " " * (width))
    print()
    print(Fore.GREEN + "[+] Tool unlocked. Opening generator in browser...")

def main():
    cwd = os.getcwd()
    outpath = os.path.join(cwd, GEN_HTML)
    write_generator(outpath)
    termux_lock_flow()
    time.sleep(1)
    ok = open_path_in_android(outpath)
    if not ok:
        print(Fore.RED + "Failed to open generator automatically. Open this file manually in your Android browser:")
        print("file://" + outpath)
    else:
        print(Fore.GREEN + "Generator opened. Use it to pick image, set password & reveal countdown, then generate the final .html.")

if __name__ == "__main__":
    main()
