import urllib.request
import string
import json
import os
import platform
from random import randint
from time import sleep
from itertools import product, chain

try:
    from bs4 import BeautifulSoup
except ImportError as e:
    print("You have missing dependencies. Run: pip install bs4 lxml")    
    exit(1)

# --- Setup ---
running = False
closeit = True
print("There are three methods for finding good names.")
print("Method 1: Random suffixes. This will put a short but random suffix to your desired name (e.g drew8n). Faster and endless but not as clean.")
print("Method 2: Predetermined suffixes. You will input the suffixes you want yourself. This is cleaner but not endless. You will have the choice to have multiple base names.")
print("Method 3: Short names. You will choose how many letters you want, and it'll scan for random names. These are rarer, but pretty cool if you get one.")
choosing = True
while choosing:
    method = input("Choose: ")
    if method == "1" or method == "2" or method == "3":
        choosing = False
        method = int(method)
    else: 
        print("Invalid. You must input either 1 or 2.")
if method == 1:
    target_base = input("Base name you want: ")
    symbols = string.digits + "._" + string.ascii_lowercase
    combinations = chain.from_iterable(product(symbols, repeat=l) for l in range(1, 6))
elif method == 2:
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
else:
    choosing = True
    symbols = string.digits + "._" + string.ascii_lowercase
    while choosing:
        amount = input("Amount of letters you want in your name: ")
        try:
            amount = int(amount)
            choosing = False
        except:
            print("Invalid. You must type a number.")

print("Starting!")
print("Ctrl+C to exit.")
sleep(1)

# --- Main Loop ---
while True:
    # This updates the name 
    if method == 1:
        suffix = "".join(next(combinations))
        if suffix[-1] == ".":  # Names can't end with "." on tiktok so we move on to the next
            suffix = "".join(next(combinations))
        current_target = target_base + suffix

    elif method == 2:
        try:
            current_target = multi[multi_counter] + suffixes[suffix_counter]
        except IndexError:
            suffix_counter = 0
            multi_counter += 1
            current_target = multi[multi_counter] + suffixes[suffix_counter]
            if multi_counter >= len(multi):
                print("Done!")
                current_target = "Thanks for using my script."
        suffix_counter += 1

    else:
        current_target = ""
        for _ in range(amount):
            current_target += symbols[randint(0, 37)] 

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
        print(f"⚠️ Could not find data for {current_target} (Possible bot detection?)")

    # TikTok will ban your IP if you go too fast, so we wait a bit
    sleep(1)
 
