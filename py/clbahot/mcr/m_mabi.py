import pyautogui
import time
import threading

macro_8_running = False

def toggle_macro_8():
    global macro_8_running
    macro_8_running = not macro_8_running
    if macro_8_running:
        print("8키 전용 매크로 ON")
        threading.Thread(target=run_macro_8).start()
    else:
        print("8키 전용 매크로 OFF")

def run_macro_8():
    while macro_8_running:
        pyautogui.press('8')
        pyautogui.press('enter')
        time.sleep(0.1)
