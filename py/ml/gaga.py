import pyautogui
import time

while True:
    for _ in range(99999):  # 2분 (120초) 동안 3초 간격으로 10번 반복

        time.sleep(3)

        # 첫번째 퀘스트 클릭
        pyautogui.moveTo(669, 551)
        time.sleep(0.2)
        pyautogui.click()

        # 가가의 선물
        time.sleep(0.2)
        pyautogui.moveTo(1200, 605)
        time.sleep(0.2)
        pyautogui.click()

         # 수락
        time.sleep(0.2)
        pyautogui.moveTo(1491, 686)
        time.sleep(0.2)
        pyautogui.click()

        # 대화그만하기
        time.sleep(0.2)
        pyautogui.moveTo(987, 690)
        time.sleep(0.2)
        pyautogui.click()

         # 두번째 퀘스트 클릭
        time.sleep(2)
        pyautogui.moveTo(669, 551)
        time.sleep(0.2)
        pyautogui.click()

         # 완료가능
        time.sleep(2)
        pyautogui.moveTo(1214, 604)
        time.sleep(0.2)
        pyautogui.click()

         # 다음
        time.sleep(2)
        pyautogui.moveTo(1533, 654)
        time.sleep(0.2)
        pyautogui.click()

         # 대화그만하기
        time.sleep(0.2)
        pyautogui.moveTo(987, 690)
        time.sleep(0.2)
        pyautogui.click()

        time.sleep(120)

print("프로그램을 종료합니다.")