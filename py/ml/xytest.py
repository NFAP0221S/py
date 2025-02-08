import pyautogui
import time

try:
    while True:
        x, y = pyautogui.position()
        print(f"1 현재 마우스 좌표: x={x}, y={y}", end='\r')  # \r은 캐리지 리턴으로, 현재 줄의 맨 앞으로 커서를 이동시킵니다.
        time.sleep(3)  # 0.1초마다 좌표를 업데이트합니다.

except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")