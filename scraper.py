import pynput.keyboard as keyboard
import string
import json
import urllib.request
import os
import platform
from time import sleep
from itertools import product, chain
from bs4 import BeautifulSoup

pip_packages = ["pynput", "bs4"]
for pkg in pip_packages:
    try:
        __import__(pkg)
    except ImportError:
        print(f"❌ {pkg} is not installed. Installing dependencies....")
        if "Windows" in platform.system():
            os.system("pip install pynput")
            os.system("pip install beautifulsoup4")
        elif "Linux" in platform.system():
            os.system("pip install pynput --break-system-packages")
            os.system("pip install beautifulsoup4 --break-system-packages")
        else:
            print("It seems your system isn't supported. The supported systems are Windows and Linux. Expect crashes.")
            sleep(3)
# --- Setup ---
running = False
closeit = True
print("There are two methods for finding good names.")
print("Method 1: Random suffixes. This will put a short but random suffix to your desired name (e.g drew8n). Faster and endless but not as clean.")
print("Method 2: Predetermined suffixes. You will input the suffixes you want yourself. This is cleaner but not endless. You will have the choice to have multiple base names.")
choosing = True
while choosing:
    method = input("Choose: ")
    if method == "1" or method == "2":
        choosing = False
        method = int(method)
    else: 
        print("Invalid. You must input either 1 or 2.")
if method == 1:
    target_base = input("Base name you want: ")
    symbols = string.digits + "._" + string.ascii_lowercase
    combinations = chain.from_iterable(product(symbols, repeat=l) for l in range(1, 6))
else:
    multi = []
    suffixes = []
    print("You have chosen method 2. Pick as many base names as you want. When you are done, input done.")
    choosing = True
    while choosing:
        choice = input("Base name you want: ")
        if choice.lower() == "done":
            choosing = False
        else:
            multi.append(choice)
    print("Now, input your suffixes. When you are done, input done.")
    choosing = True
    while choosing:
        choice = input("Suffix you want: ")
        if choice.lower() == "done":
            choosing = False
        else:
            suffixes.append(choice)
    multi_counter = 0
    suffix_counter = 0

def on_press(key):  # This handles our hotkeys for pausing and exiting
    global running, closeit
    try:
        if key.char.lower() == 'q':
            running = not running
            print("\n[Paused/Started]")
        if key.char.lower() == 'r':
            running = False
            closeit = False
            print("\n[Program exited]")
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

print("Press 'Q' to start/pause, 'R' to exit.")

# --- Main Loop ---
while closeit:
    if running:
        # This updates the name 
        if method == 1:
            suffix = "".join(next(combinations))
            if suffix[-1] == ".":  # Names can't end with "." on tiktok so we move on to the next
                suffix = "".join(next(combinations))
            current_target = target_base + suffix
        else:
            try:
                current_target = multi[multi_counter] + suffixes[suffix_counter]
            except IndexError:
                suffix_counter = 0
                multi_counter += 1
                current_target = multi[multi_counter] + suffixes[suffix_counter]
                if multi_counter >= len(multi):
                    running = False
                    print("Done!")
                    current_target == "Thanks for using my script."
            suffix_counter += 1
        
        url = f"https://www.tiktok.com/@{current_target}"
       
        # This sets up the headers so we dont get blocked
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36'
        })

        # This fetches the page
        with urllib.request.urlopen(req) as response:
            html = response.read()
            soup = BeautifulSoup(html, "lxml")

        # This gives us the JSON data
        script_tag = soup.find("script", id="__UNIVERSAL_DATA_FOR_REHYDRATION__")
        
        if script_tag:
            script_json = json.loads(script_tag.string)
            # This looks for the status code
            user_data = script_json.get("__DEFAULT_SCOPE__", {}).get("webapp.user-detail", {})
            status_code = user_data.get("statusCode")

            if status_code == 10202 or status_code == 10221:
                print(f"✅ {current_target} is AVAILABLE")
            elif status_code == 0 or status_code == 10222:
                print(f"❌ {current_target} is TAKEN")
            else:
                print(f"❓ {current_target} returned unknown status: {status_code}")
        else:
            print(f"⚠️ Could not find data for {current_target} (Bot detection?)")

            # TikTok will ban your IP if you go too fast, so we wait a bit
            sleep(1.5) 
    else:
        sleep(0.25)