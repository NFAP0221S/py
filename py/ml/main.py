import pyautogui
import time
import keyboard  # keyboard 라이브러리 추가

t = 0.2
c = 12
for _ in range(c):
    if keyboard.is_pressed('space'):  # 스페이스바가 눌렸는지 확인
        print("스페이스바가 눌러져 프로그램을 종료합니다.")
        break  # 반복문 탈출

    # 찰리중사 클릭
    pyautogui.moveTo(868, 91)
    time.sleep(t)
    pyautogui.doubleClick()

    # 찰리중사 다음
    pyautogui.moveTo(1121, 450)
    time.sleep(t)
    pyautogui.click()

    # 찰리중사 예
    pyautogui.moveTo(1109, 519)
    time.sleep(t)
    pyautogui.click()

    # 중간 텀
    time.sleep(t)

    # 찰리중사 보조 스크롤이동
    pyautogui.moveTo(1177, 263)
    time.sleep(t)
    pyautogui.click()

    # 찰리중사 스크롤이동
    pyautogui.moveTo(1177, 417)
    time.sleep(t)
    pyautogui.click()

    # 중간 텀
    time.sleep(t)

    # 찰리중사 스크롤이동
    pyautogui.moveTo(914, 426)
    time.sleep(t)
    pyautogui.click()

    # 찰리중사 예
    pyautogui.moveTo(1109, 519)
    time.sleep(t)
    pyautogui.click()

    time.sleep(t)
    pyautogui.press('esc')
    print("지정된 좌표에서 더블 클릭을 완료했습니다.")

print("프로그램을 종료합니다.")