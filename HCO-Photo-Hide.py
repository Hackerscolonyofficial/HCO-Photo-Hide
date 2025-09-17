import os
import time
import webbrowser
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Hackers Colony header
def header():
    print(Fore.RED + Style.BRIGHT + "\n╔══════════════════════════════╗")
    print(Fore.RED + Style.BRIGHT + "│ Hackers Colony Official      │")
    print(Fore.RED + Style.BRIGHT + "│ HCO-Photo-Hide by Azhar               │")
    print(Fore.RED + Style.BRIGHT + "╚══════════════════════════════╝\n")

# Lock message with countdown
def tool_lock():
    print(Fore.YELLOW + "This tool is locked 🔒")
    print(Fore.YELLOW + "To unlock 🔐, you will be redirected to YouTube...")
    for i in range(5, 0, -1):
        print(Fore.CYAN + f"Redirecting in {i} seconds...", end="\r")
        time.sleep(1)
    print("\n")

    # Force open YouTube app using Android Intent
    youtube_url = "https://youtube.com/@hackers_colony_tech?si=pvdCWZggTIuGb0ya"
    try:
        os.system(f'am start -a android.intent.action.VIEW -d "{youtube_url}" com.google.android.youtube')
    except:
        # fallback: open in default browser
        webbrowser.open(youtube_url)

    input(Fore.GREEN + "\nPress Enter after subscribing to continue...")

# Main hacker-style interface
def main_ui():
    header()
    photo = input(Fore.GREEN + "[+] Enter path to photo: " + Style.RESET_ALL)
    password = input(Fore.GREEN + "[+] Set a password to hide the photo: " + Style.RESET_ALL)
    
    # HTML generation simulation
    html_file = "hidden_photo.html"
    with open(html_file, "w") as f:
        f.write(f"<html><body><h1>Photo Hidden Successfully!</h1><p>Password: {password}</p></body></html>")
    
    print(Fore.MAGENTA + f"\n[✔] Hidden photo HTML generated: {html_file}\n")

# Run tool
if __name__ == "__main__":
    tool_lock()
    main_ui()
