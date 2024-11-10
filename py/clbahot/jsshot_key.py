import pyautogui
import time
from pynput import keyboard
import threading

# 매크로 상태를 저장하는 변수
macro_running = False
macro_8_running = False
macro_9_running = False
macro_paused = False  # 전체 매크로 일시중지 상태
ctrl_pressed = False  # Ctrl 키 상태 추적
shift_pressed = False  # Shift 키 상태 추적

def toggle_macro():
    global macro_running
    macro_running = not macro_running
    if macro_running:
        print("기본 매크로 ON")
        threading.Thread(target=execute_macro).start()
    else:
        print("기본 매크로 OFF")

def execute_macro():
    while macro_running:
        if not macro_paused:
            # 여기에 매크로가 실행 중일 때 반복할 동작을 정의합니다.
            pyautogui.press('8')
            pyautogui.press('enter')
            pyautogui.press('8')
            pyautogui.press('enter')
            pyautogui.press('8')
            pyautogui.press('enter')
            time.sleep(0.1)
        else:
            time.sleep(0.1)

def toggle_macro_8():
    global macro_8_running
    macro_8_running = not macro_8_running
    if macro_8_running:
        print("8키 전용 매크로 ON")
        threading.Thread(target=run_macro_8).start()
    else:
        print("8키 전용 매크로 OFF")

def toggle_macro_9():
    global macro_9_running
    macro_9_running = not macro_9_running
    if macro_9_running:
        print("9키 전용 매크로 ON")
        threading.Thread(target=run_macro_9).start()
    else:
        print("9키 전용 매크로 OFF")

def toggle_pause_all():
    global macro_paused
    macro_paused = not macro_paused
    if macro_paused:
        print("모든 매크로 일시 중지")
    else:
        print("모든 매크로 재개")

def run_macro_8():
    while macro_8_running and not macro_paused:
        pyautogui.press('8')
        pyautogui.press('enter')
        pyautogui.press('8')
        pyautogui.press('enter')
        pyautogui.press('8')
        pyautogui.press('enter')
        time.sleep(0.1)

def run_macro_9():
    while macro_9_running and not macro_paused:
        pyautogui.press('7')
        pyautogui.press('enter')
        pyautogui.press('7')
        pyautogui.press('enter')
        pyautogui.press('7')
        pyautogui.press('enter')
        time.sleep(0.1)

def on_press(key):
    global ctrl_pressed, shift_pressed
    
    if key == keyboard.Key.ctrl:
        ctrl_pressed = True
    elif key == keyboard.Key.shift:
        shift_pressed = True
    elif key == keyboard.KeyCode.from_char('v'):
        if ctrl_pressed and not shift_pressed:
            toggle_macro_8()
        elif ctrl_pressed and shift_pressed:
            toggle_macro_9()
    
    try:
        if key.char == '[':
            toggle_macro()  # 기본 매크로 on/off 전환
    except AttributeError:
        if key == keyboard.Key.esc:
            toggle_pause_all()

def on_release(key):
    global ctrl_pressed, shift_pressed

    if key == keyboard.Key.ctrl:
        ctrl_pressed = False
    elif key == keyboard.Key.shift:
        shift_pressed = False

# 리스너 설정
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("기본 매크로: 시작/종료는 [ 키")
    print("8키 전용 매크로: 시작/종료는 Ctrl + V 키")
    print("9키 전용 매크로: 시작/종료는 Ctrl + Shift + V 키")
    print("전체 매크로 일시 중지/재개는 ESC 키")
    listener.join()
