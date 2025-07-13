import network
import urequests as requests
import machine
import time
import json

from secrets import SSID, PASSWORD

GITHUB_API_URL = "https://api.github.com/repos/irigon/ota_esp32/contents/src"
RAW_BASE_URL = "https://raw.githubusercontent.com/irigon/ota_esp32/master/src"
headers = {
    "User-Agent": "ESP32-MicroPython"
}

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    # Wifi state can get stuck if reinitiated multiple times: set to False and then True
    sta.active(False)
    time.sleep(1)
    sta.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        print("Wi-Fi connected:", wlan.ifconfig())
    else:
        raise RuntimeError("Wi-Fi connection failed.")

def fetch_file_list():
    try:
        print("Fetching file list from GitHub...")
        r = requests.get(GITHUB_API_URL, headers=headers)
        if r.status_code == 200:
            # Get all files of interest. Secrets.py is ignored, it should be updated locally
            return [file['name'] for file in r.json() if file['type'] == 'file' and file['name'] != "secrets.py"]
        else:
            print("Failed to fetch file list:", r.status_code, r.text)
            return []
    except Exception as e:
        print("Error during file list fetch:", e)
        return []

def download_file(name):
    try:
        url = f"{RAW_BASE_URL}/{name}"
        print(f"Downloading {url}...")
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            with open(name, "w") as f:
                f.write(r.text)
            print(f"Updated: {name}")
        else:
            print(f"Failed to download {name}: status {r.status_code}")
        r.close()
    except Exception as e:
        print(f"Error downloading {name}: {e}")

def run_ota():
    try:
        connect_wifi()
        files = fetch_file_list()
        if not files:
            print("No files to update.")
            return
        for fname in files:
            download_file(fname)
        print("OTA update complete. Rebooting...")
        time.sleep(2)
        machine.reset()
    except Exception as e:
        print("OTA update failed:", e)

