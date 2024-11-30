# macros/macro_ddp.py

import pyautogui

class MacroDDP:
    def __init__(self, log_function):
        self.log = log_function

    def execute(self):
        self.log("동동필 매크로 실행: ~키 입력")
        pyautogui.press('u')
        pyautogui.press('u')
        pyautogui.press('u')
        pyautogui.press('u')
        pyautogui.press('6')
