import time
import cv2
import numpy as np
import pyautogui

def 시작_MP모니터링(low_items):
    # MP 모니터링 루프
    while low_items[2]["monitoring"]:
        mp_area = low_items[2]["mp_area"]
        입력값_위젯 = low_items[2]["value"]
        로그_텍스트 = low_items[2]["log_text"]

        x1, y1, x2, y2 = mp_area
        스크린샷 = pyautogui.screenshot()
        frame = np.array(스크린샷)
        mp_bar = frame[y1:y2, x1:x2]
        gray = cv2.cvtColor(mp_bar, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        white_pixels = cv2.countNonZero(thresh)
        total_pixels = mp_bar.shape[0] * mp_bar.shape[1]
        mp_percentage = (white_pixels / total_pixels) * 100

        try:
            input_value = float(입력값_위젯.get())
            adjusted_mp_percentage = (mp_percentage / input_value) * 100
            log_message = f"조정된 MP: {adjusted_mp_percentage:.2f}%"
        except ValueError:
            log_message = f"현재 MP: {mp_percentage:.2f}%"

        print(log_message)

        로그_텍스트.config(state="normal")
        로그_텍스트.insert("end", log_message + "\n")
        로그_텍스트.see("end")
        로그_텍스트.config(state="disabled")

        time.sleep(1)
