import network
import urequests as requests
import machine
import time
import json

from secrets import SSID, PASSWORD

GITHUB_API_URL = "https://api.github.com/repos/irigon/ota_esp32/contents/src"
RAW_BASE_URL = "https://raw.githubusercontent.com/irigon/ota_esp32/master/src"
LOCAL_VERSION_FILE = "version.txt"

headers = {
    "User-Agent": "ESP32-MicroPython"
}

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
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
            print(f"Failed to fetch file list: {r}")
            return []
    except Exception as e:
        print("Error during file list fetch:", e)
        return []

def download_file(name):
    try:
        url = f"{RAW_BASE_URL}/{name}"
        print(f"Downloading {url}...")
        r = requests.get(url)
        if r.status_code == 200:
            with open(name, "w") as f:
                f.write(r.text)
            print(f"Updated: {name}")
        else:
            print(f"Failed to download {name}: status {r.status_code}, text: {r.text}")
        r.close()
    except Exception as e:
        print(f"Error downloading {name}: {e}")

def get_local_version():
    try:
        with open(LOCAL_VERSION_FILE) as f:
            return f.read().strip()
    except OSError:
        return "0.0.0"

def get_remote_version():
    try:
        response = urequests.get(REMOTE_VERSION_URL)
        if response.status_code == 200:
            return response.text.strip()
    except Exception as e:
        print("Failed to fetch remote version:", e)
    return None

def is_update_needed():
    local = get_local_version()
    remote = get_remote_version()
    print(f"Local version: {local}, Remote version: {remote}")
    if remote is None:
        return False
    return remote > local  # simple string comparison, e.g. "1.2.1" > "1.1.9"

def update_local_version(remote_version):
    with open(LOCAL_VERSION_FILE, "w") as f:
        f.write(remote_version)

