from pynput import keyboard
from mcr.base_macro import toggle_macro
from mcr.m_mabi import toggle_macro_8
from mcr.m_joongdok import toggle_macro_9
from mcr.controls import toggle_pause_all, stop_all_macros

ctrl_pressed = False
shift_pressed = False

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
            stop_all_macros()  # ESC 키로 모든 매크로 종료

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
    print("전체 매크로 종료는 ESC 키")
    listener.join()
