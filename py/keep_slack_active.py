import pyautogui
import time

def keep_slack_active(interval=5):
    try:
        while True:
            # 마우스를 살짝 움직여줍니다.
            pyautogui.moveRel(0, 100, duration=0.5)  # 아래로 10픽셀
            pyautogui.moveRel(0, -100, duration=0.5)  # 원래 위치로 이동

            # 지정된 시간 동안 대기합니다.
            time.sleep(interval)
    except KeyboardInterrupt:
        print("프로그램이 중지되었습니다.")

if __name__ == "__main__":
    keep_slack_active()