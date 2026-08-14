"""Night-shift keep-awake: prevents Windows sleep ONLY while running (app-level,
reversible — like a video player). Self-exits at END_HOUR local time.

Run: .venv/Scripts/python.exe -u tools/keep_awake.py
"""

import ctypes
import datetime
import time

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
END_HOUR = 8  # local

print("keep-awake ON (system sleep prevented while this runs)", flush=True)
try:
    while True:
        now = datetime.datetime.now()
        if now.hour >= END_HOUR and now.hour < 22:
            break
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
        time.sleep(50)
finally:
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    print("keep-awake OFF (normal power behavior restored)", flush=True)
