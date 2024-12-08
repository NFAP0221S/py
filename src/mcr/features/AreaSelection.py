import cv2
import numpy as np
import pyautogui
from tkinter import messagebox
import easyocr

# EasyOCR Reader 생성 (영어, 한국어 예시)
# 필요 언어에 따라 ['en', 'ko'] 등으로 변경 가능
reader = easyocr.Reader(['ko'], verbose=False)

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

            # 영역 설정 완료 후 각 idx에 따라 다른 기능 실행
            if idx == 1:
                # 2번째 로우: 영역 내 텍스트 및 숫자 인식 후 로그 출력
                영역2_텍스트_로그_출력(low_items, idx)

    cv2.namedWindow("영역 설정", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("영역 설정", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("영역 설정", frame)
    cv2.setMouseCallback("영역 설정", 마우스_이벤트)
    cv2.waitKey(0)

def 영역2_텍스트_로그_출력(low_items, idx):
    area = low_items[idx].get("mp_area")
    if area:
        x1, y1, x2, y2 = area
        스크린샷 = pyautogui.screenshot()
        frame = np.array(스크린샷)
        crop = frame[y1:y2, x1:x2]

        # 전처리 과정(필요하다면 추가)
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # EasyOCR로 텍스트 인식
        result_ocr = reader.readtext(thresh)

        if result_ocr:
            recognized_text = result_ocr[0][1].strip()
        else:
            recognized_text = ""

        # 전체 텍스트 출력
        log_text = low_items[idx]["log_text"]
        log_text.config(state="normal")
        log_text.insert("end", f"영역2 텍스트 인식 결과: {recognized_text}\n")
        
        # 숫자만 추출 (원한다면)
        digits_only = ''.join([c for c in recognized_text if c.isdigit()])
        if digits_only:
            log_text.insert("end", f"영역2 숫자 인식 결과: {digits_only}\n")

        log_text.see("end")
        log_text.config(state="disabled")
