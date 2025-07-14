# OTA Updates for ESP32

This repository contains code for Over-The-Air (OTA) updates on ESP32 devices using MicroPython. The main components include a boot script that checks for updates and an OTA module that handles the update process.

Its aim is to provide a simple and effective way to keep your ESP32 firmware up-to-date that can be easily integrated on other repositories.

## How to develop
1. Clone the repository.
2. Modify the code according to your needs.
3. Bump the version in `versions.txt`
4. Restart the ESP32.
    - During its reboot, it will check for updates and apply them if necessary.

## How it works
There are two main scripts:
- `boot.py`: Runs once during the initialization of the ESP32. It connects to Wi-Fi, checks if an update is needed, and if so, it downloads and applies the update.
- `main.py`: Executes the main logic.

`boot.py` relies on the `ota.py` module, which contains functions required for the update (to connect to Wi-Fi, check for updates, and download files).

The Wi-Fi credentials are stored in secrets.py (following the template secrets.py.template)

## Tips
There are a few scripts that are used to simplify the development. They are packed into the Makefile.
The following commands are available:
- `make clean`: Cleans the build directory, and removes all files from the ESP32 root directory.
- `make compile`: Copies all .py and .txt files from the `src` directory to the build directory, and compiles them into .mpy files except for `boot.py`, `main.py`, and `version.txt`. .mpy files load faster on the ESP32 (they are already bytecode), have reduced size, obfuscate the code and use less RAM at runtime.
- `make flash`: Uploads the files from the build directority to the ESP32.
- `make repl`: Opens a REPL session on the ESP32. To reset the device, use `import machine; machine.reset()`.
- `mpremote`: Useful command lines
    ````bash
    mpremote connect /dev/ttyUSB0 fs ls
    mpremote connect /dev/ttyUSB0 fs cat boot.py
    mpremote connect /dev/ttyUSB0 fs rm version.txt
    ````