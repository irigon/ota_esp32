import ota
import time

try:
    ota.connect_wifi()
    if ota.is_update_needed():
        files = ota.fetch_file_list()
        if files:
            for fname in files:
                ota.download_file(fname)
            print("OTA update complete. Rebooting...")
            time.sleep(2)
            machine.reset()
    else:
        print("No OTA update needed.")
except Exception as e:
    print("OTA update failed:", e)

    ota.update_local_version(ota.get_remote_version())

