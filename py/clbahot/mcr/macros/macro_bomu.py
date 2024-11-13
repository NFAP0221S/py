# macros/macro_bomu.py

import time
import pyautogui
import threading

class MacroBomu:
    def __init__(self, log_function, update_indicator_func):
        self.running = False
        self.log = log_function
        self.update_indicator = update_indicator_func
        self.thread = None
        self.stop_event = threading.Event()

    def toggle(self):
        self.running = not self.running
        if self.running:
            self.log("Bomu 매크로 ON")
            self.update_indicator(True)
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
        else:
            self.log("Bomu 매크로 OFF")
            self.update_indicator(False)
            self.stop_event.set()
            if self.thread:
                self.thread.join()

    def run(self):
        try:
            while not self.stop_event.is_set():
                self.log("Bomu 매크로 실행: 9, home, enter, 0, enter 키 입력")
                time.sleep(2)
                pyautogui.press('9')
                pyautogui.press('home')
                pyautogui.press('enter')
                pyautogui.press('0')
                pyautogui.press('enter')
                # 186초 대기
                self.stop_event.wait(15)
        except Exception as e:
            self.log(f"Bomu 매크로 오류: {e}")
            self.running = False
            self.update_indicator(False)
