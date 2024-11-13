# macros/macro_q.py

import pyautogui

class MacroQ:
    def __init__(self, log_function):
        self.log = log_function

    def execute(self):
        self.log("Q 매크로 실행: 8 키 입력")
        pyautogui.press('8')
        # 추가로 'enter' 키가 필요하면 아래 주석을 해제하세요
        # pyautogui.press('enter')
