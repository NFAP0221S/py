# macros/macro_8.py

import threading
import pyautogui

class Macro9:
    def __init__(self, log_function, update_indicator_func):
        self.running = False
        self.log = log_function
        self.update_indicator = update_indicator_func

    def toggle(self, force_off=False):
        if not force_off and not self.running:
            self.running = True
            self.log("9키 매크로 ON")
            self.update_indicator(True)
            threading.Thread(target=self.execute, daemon=True).start()
        elif force_off and self.running:
            self.running = False
            self.log("9키 매크로 OFF")
            self.update_indicator(False)
        else:
            self.running = not self.running
            if self.running:
                self.log("9키 매크로 ON")
                self.update_indicator(True)
                threading.Thread(target=self.run, daemon=True).start()
            else:
                self.log("9키 매크로 OFF")
                self.update_indicator(False)

    def execute(self):
        self.log("9매크로 실행")
        pyautogui.press('7')
        pyautogui.press('left')
        pyautogui.press('enter')

        pyautogui.press('7')
        pyautogui.press('left')
        pyautogui.press('enter')
        pyautogui.press('7')
        pyautogui.press('left')
        pyautogui.press('enter')
        pyautogui.press('7')
        pyautogui.press('left')
        pyautogui.press('enter')
