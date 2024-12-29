import pyautogui
import cv2
import numpy as np
import time
from skimage.metrics import structural_similarity as ssim
import tkinter as tk
from tkinter import messagebox

def calculate_similarity(roi1, roi2):
    if roi1 is None or roi2 is None or roi1.size == 0 or roi2.size == 0:
        return False
    
    # 두 이미지의 평균값 계산
    avg1 = np.mean(roi1)
    avg2 = np.mean(roi2)
    
    # 평균값이 비슷한지 확인 (약간의 오차 허용)
    return abs(avg1 - avg2) < 5  # 오차 범위는 조절 가능

def select_roi_drag(frame, window_title):
    x1, y1 = -1, -1
    drawing = False
    roi = None
    roi_coords = None
    temp_frame = frame.copy()  # 표시용 프레임
    original_frame = frame.copy()  # 원본 프레임 저장

    def draw_rectangle(event, x, y, flags, param):
        nonlocal x1, y1, drawing, roi, roi_coords, temp_frame
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            x1, y1 = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                frame[:] = temp_frame
                cv2.rectangle(frame, (x1, y1), (x, y), (0, 255, 0), 2)
                cv2.imshow(window_title, frame)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            x2, y2 = x, y
            # 화면 표시용 사각형
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.imshow(window_title, frame)
            
            # 좌표 계산
            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)
            # 원본 이미지에서 ROI 추출
            roi = original_frame[y_min:y_max, x_min:x_max]
            roi_coords = (x_min, y_min, x_max - x_min, y_max - y_min)
            
            if roi is not None and roi.size != 0:
                cv2.imshow("Selected ROI", roi)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                cv2.destroyAllWindows()

    cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_title, frame)
    cv2.setMouseCallback(window_title, draw_rectangle)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q') or roi is not None:
            break
    cv2.destroyAllWindows()
    return roi, roi_coords

# Tkinter root 생성 (숨김)
root = tk.Tk()
root.withdraw()

# 스크린샷 캡쳐
screenshot = pyautogui.screenshot()
frame = np.array(screenshot)
frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

# 체력바 영역 지정
messagebox.showinfo("알림", "체력바 영역을 지정해주세요.")
roi, roi_coords = select_roi_drag(frame.copy(), "체력바 영역 선택")

if roi is None or roi.size == 0:
    print("체력바 영역이 선택되지 않았습니다. 프로그램을 종료합니다.")
    exit()

print("체력바 영역이 설정되었습니다.")

# 첫 번째 페이즈: 영역 기억
messagebox.showinfo("알림", "영역을 기억했습니다. 확인을 누르면 모니터링을 시작합니다.")
stored_roi = roi  # 원본 이미지 그대로 저장
print("영역을 기억했습니다.")

# 저장된 이미지 보여주기
cv2.imshow("Stored Image", stored_roi)
cv2.waitKey(1)  # 이미지 창을 업데이트하기 위한 대기

# 두 번째 페이즈: 영역 모니터링
messagebox.showinfo("알림", "체력바 영역을 모니터링합니다.")
print("체력바 영역 모니터링 시작.")

# 첫 번째 모니터링 이미지 캡처 및 표시
screenshot = pyautogui.screenshot()
frame = np.array(screenshot)
frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
x, y, w, h = roi_coords
current_roi = frame[y:y+h, x:x+w]
cv2.imshow("Current Image", current_roi)
cv2.waitKey(0)  # 사용자가 키를 누를 때까지 대기
cv2.destroyAllWindows()

while True:
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    try:
        x, y, w, h = roi_coords
        # ROI 추출 전에 범위 확인
        if x >= 0 and y >= 0 and x + w <= frame.shape[1] and y + h <= frame.shape[0]:
            current_roi = frame[y:y+h, x:x+w]
            is_same = calculate_similarity(stored_roi, current_roi)
            
            if not is_same:
                print("체력이 없습니다.")
            else:
                print("변화 없음")
        else:
            print("ROI 좌표가 이미지 범위를 벗어납니다. 다시 영역을 지정해주세요.")
            break
    except Exception as e:
        print(f"에러 발생: {e}")
        break

    time.sleep(0.5)