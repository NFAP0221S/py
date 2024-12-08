import cv2
import numpy as np
import pyautogui
from tkinter import messagebox

def 영역_선택(idx, 메시지, low_items):
    # 화면 캡처 후 영역 선택
    화면_너비, 화면_높이 = pyautogui.size()
    스크린샷 = pyautogui.screenshot()
    frame = np.array(스크린샷)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    overlay = frame.copy()
    alpha = 0.3
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    x1, y1 = -1, -1
    drawing = False

    def 마우스_이벤트(event, x, y, flags, param):
        nonlocal x1, y1, drawing, frame
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            x1, y1 = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                temp_frame = frame.copy()
                cv2.rectangle(temp_frame, (x1, y1), (x, y), (0, 255, 0), 2)
                cv2.imshow("영역 설정", temp_frame)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            x2, y2 = x, y
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.imshow("영역 설정", frame)
            low_items[idx]["mp_area"] = (x1, y1, x2, y2)
            cv2.destroyAllWindows()
            messagebox.showinfo("영역 선택", 메시지)

    cv2.namedWindow("영역 설정", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("영역 설정", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("영역 설정", frame)
    cv2.setMouseCallback("영역 설정", 마우스_이벤트)
    cv2.waitKey(0)
