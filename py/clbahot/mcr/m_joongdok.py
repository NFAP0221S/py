import pyautogui
import time
import threading

macro_9_running = False

def toggle_macro_9():
    global macro_9_running
    macro_9_running = not macro_9_running
    if macro_9_running:
        print("9키 전용 매크로 ON")
        threading.Thread(target=run_macro_9).start()
    else:
        print("9키 전용 매크로 OFF")

def run_macro_9():
    while macro_9_running:
        pyautogui.press('7')
        pyautogui.press('enter')
        time.sleep(0.1)
