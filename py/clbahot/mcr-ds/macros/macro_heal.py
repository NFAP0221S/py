# macros/macro_heal.py

import pyautogui

class MacroHeal:
    def __init__(self, log_function):
        self.log = log_function

    def execute(self):
        self.log("힐 매크로 실행: ~키 입력")
        pyautogui.press('esc')
        pyautogui.press('1')
        pyautogui.press('home')
        pyautogui.press('enter')
        pyautogui.press('1')
        pyautogui.press('enter')
