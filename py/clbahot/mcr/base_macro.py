import pyautogui
import time
import threading
from controls import toggle_pause_all

macro_running = False
macro_paused = False

def toggle_macro():
    global macro_running
    macro_running = not macro_running
    if macro_running:
        print("기본 매크로 ON")
        threading.Thread(target=execute_macro).start()
    else:
        toggle_pause_all()
        print("기본 매크로 OFF")

def execute_macro():
    while macro_running:
        if not macro_paused:
            pyautogui.press('8')
            pyautogui.press('enter')
            time.sleep(0.1)
        else:
            time.sleep(0.1)
