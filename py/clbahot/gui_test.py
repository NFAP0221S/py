import tkinter as tk
import pyautogui
import time
import threading
from tkinter.scrolledtext import ScrolledText
from pynput import keyboard

# 매크로 상태를 저장하는 변수
macro_running = False
macro_7_running = False
macro_8_running = False
macro_ctrl1_running = False
macro_ctrl2_running = False
macro_ctrl3_running = False
log_index = 1  # 로그 인덱스 초기화

# 키보드 상태를 추적하기 위한 집합
pressed_keys = set()
toggled_combinations = set()

# 로그를 기록하는 함수
def log_message(message):
    global log_index
    log_text.config(state='normal')
    log_text.insert(tk.END, f"{log_index}번째 Log: {message}\n")
    log_text.config(state='disabled')
    log_text.yview(tk.END)  # 로그 화면이 자동으로 스크롤되도록 설정
    log_index += 1  # 인덱스를 증가

def update_indicator(indicator, state):
    color = "green" if state else "red"
    indicator.itemconfig(indicator.find_withtag("circle"), fill=color)

# 모든 매크로를 끄는 함수 (기본 매크로 제외)
def turn_off_all_macros(exclude=None):
    global macro_7_running, macro_8_running
    global macro_ctrl1_running, macro_ctrl2_running, macro_ctrl3_running

    if exclude != '7':
        if macro_7_running:
            toggle_macro_7(force_off=True)
    if exclude != '8':
        if macro_8_running:
            toggle_macro_8(force_off=True)
    if exclude != 'ctrl1':
        if macro_ctrl1_running:
            toggle_macro_ctrl('1', force_off=True)
    if exclude != 'ctrl2':
        if macro_ctrl2_running:
            toggle_macro_ctrl('2', force_off=True)
    if exclude != 'ctrl3':
        if macro_ctrl3_running:
            toggle_macro_ctrl('3', force_off=True)

# 기본 매크로 ON/OFF 토글 함수
def toggle_macro():
    global macro_running, macro_7_running, macro_8_running
    global macro_ctrl1_running, macro_ctrl2_running, macro_ctrl3_running

    macro_running = not macro_running
    if macro_running:
        log_message("기본 매크로 ON")
        base_macro_btn.config(bg="#4D4D4D", text="기본 매크로 OFF")  # 어두운 회색
        update_indicator(base_macro_indicator, True)
        
        # Control + 숫자 매크로 버튼 활성화
        macro_ctrl1_btn.config(state='normal')
        macro_ctrl2_btn.config(state='normal')
        macro_ctrl3_btn.config(state='normal')
    else:
        # 기본 매크로가 OFF되면 모든 매크로 OFF
        macro_running = False
        macro_7_running = False
        macro_8_running = False
        macro_ctrl1_running = False
        macro_ctrl2_running = False
        macro_ctrl3_running = False
        log_message("기본 매크로 OFF")
        base_macro_btn.config(bg="#A9DFBF", text="기본 매크로 ON")  # 밝은 초록색
        update_indicator(base_macro_indicator, False)
        
        # 7키와 8키 매크로도 OFF 상태로 전환
        macro_7_btn.config(bg="#F1948A", text="7키 매크로 ON")  # 밝은 빨간색
        update_indicator(macro_7_indicator, False)
        macro_8_btn.config(bg="#85C1E9", text="8키 매크로 ON")  # 밝은 파란색
        update_indicator(macro_8_indicator, False)
        
        # Control + 숫자 매크로도 OFF 상태로 전환
        macro_ctrl1_btn.config(bg="#D7BDE2", text="Control +1 매크로 ON", state='disabled')  # 밝은 보라색
        update_indicator(macro_ctrl1_indicator, False)
        macro_ctrl2_btn.config(bg="#F9E79F", text="Control +2 매크로 ON", state='disabled')  # 밝은 노란색
        update_indicator(macro_ctrl2_indicator, False)
        macro_ctrl3_btn.config(bg="#F5B7B1", text="Control +3 매크로 ON", state='disabled')  # 밝은 핑크색
        update_indicator(macro_ctrl3_indicator, False)

# 8키 전용 매크로 ON/OFF 토글 함수
def toggle_macro_8(force_off=False):
    global macro_8_running, macro_7_running
    if not force_off and macro_running:  # 기본 매크로가 켜진 상태에서만 8키 매크로 ON/OFF 가능
        if not macro_8_running:
            # 다른 매크로 상태를 False로 설정
            turn_off_all_macros(exclude='8')
        
        macro_8_running = not macro_8_running
        if macro_8_running:
            log_message("8키 전용 매크로 ON")
            macro_8_btn.config(bg="#5DADE2", text="8키 매크로 OFF")  # 어두운 파란색
            update_indicator(macro_8_indicator, True)
            threading.Thread(target=run_macro_8, daemon=True).start()
        else:
            log_message("8키 전용 매크로 OFF")
            macro_8_btn.config(bg="#85C1E9", text="8키 매크로 ON")  # 밝은 파란색
            update_indicator(macro_8_indicator, False)
    elif force_off and macro_8_running:
        macro_8_running = False
        log_message("8키 전용 매크로 OFF")
        macro_8_btn.config(bg="#85C1E9", text="8키 매크로 ON")  # 밝은 파란색
        update_indicator(macro_8_indicator, False)

def run_macro_8():
    while macro_8_running:
        pyautogui.press('8')
        pyautogui.press('enter')
        time.sleep(0.1)

# 7키 전용 매크로 ON/OFF 토글 함수
def toggle_macro_7(force_off=False):
    global macro_7_running, macro_8_running
    if not force_off and macro_running:  # 기본 매크로가 켜진 상태에서만 7키 매크로 ON/OFF 가능
        if not macro_7_running:
            # 다른 매크로 상태를 False로 설정
            turn_off_all_macros(exclude='7')
        
        macro_7_running = not macro_7_running
        if macro_7_running:
            log_message("7키 전용 매크로 ON")
            macro_7_btn.config(bg="#CD6155", text="7키 매크로 OFF")  # 어두운 빨간색
            update_indicator(macro_7_indicator, True)
            threading.Thread(target=run_macro_7, daemon=True).start()
        else:
            log_message("7키 전용 매크로 OFF")
            macro_7_btn.config(bg="#F1948A", text="7키 매크로 ON")  # 밝은 빨간색
            update_indicator(macro_7_indicator, False)
    elif force_off and macro_7_running:
        macro_7_running = False
        log_message("7키 전용 매크로 OFF")
        macro_7_btn.config(bg="#F1948A", text="7키 매크로 ON")  # 밝은 빨간색
        update_indicator(macro_7_indicator, False)

def run_macro_7():
    while macro_7_running:
        pyautogui.press('7')
        pyautogui.press('enter')
        time.sleep(0.1)

# Control + 숫자 매크로 토글 함수
def toggle_macro_ctrl(number, force_off=False):
    global macro_ctrl1_running, macro_ctrl2_running, macro_ctrl3_running

    if not macro_running and not force_off:
        log_message(f"기본 매크로가 꺼져 있어 Control +{number} 매크로를 사용할 수 없습니다.")
        return

    if not force_off:
        if number == '1' and not macro_ctrl1_running:
            turn_off_all_macros(exclude='ctrl1')
        elif number == '2' and not macro_ctrl2_running:
            turn_off_all_macros(exclude='ctrl2')
        elif number == '3' and not macro_ctrl3_running:
            turn_off_all_macros(exclude='ctrl3')

    if number == '1':
        if force_off:
            if macro_ctrl1_running:
                macro_ctrl1_running = False
                log_message("Control +1 매크로 OFF")
                macro_ctrl1_btn.config(bg="#D7BDE2", text="Control +1 매크로 ON")
                update_indicator(macro_ctrl1_indicator, False)
        else:
            macro_ctrl1_running = not macro_ctrl1_running
            if macro_ctrl1_running:
                log_message("Control +1 매크로 ON")
                macro_ctrl1_btn.config(bg="#8E44AD", text="Control +1 매크로 OFF")  # 어두운 보라색
                update_indicator(macro_ctrl1_indicator, True)
                threading.Thread(target=run_macro_ctrl1, daemon=True).start()
            else:
                log_message("Control +1 매크로 OFF")
                macro_ctrl1_btn.config(bg="#D7BDE2", text="Control +1 매크로 ON")  # 밝은 보라색
                update_indicator(macro_ctrl1_indicator, False)

    elif number == '2':
        if force_off:
            if macro_ctrl2_running:
                macro_ctrl2_running = False
                log_message("Control +2 매크로 OFF")
                macro_ctrl2_btn.config(bg="#F9E79F", text="Control +2 매크로 ON")
                update_indicator(macro_ctrl2_indicator, False)
        else:
            macro_ctrl2_running = not macro_ctrl2_running
            if macro_ctrl2_running:
                log_message("Control +2 매크로 ON")
                macro_ctrl2_btn.config(bg="#F1C40F", text="Control +2 매크로 OFF")  # 어두운 노란색
                update_indicator(macro_ctrl2_indicator, True)
                threading.Thread(target=run_macro_ctrl2, daemon=True).start()
            else:
                log_message("Control +2 매크로 OFF")
                macro_ctrl2_btn.config(bg="#F9E79F", text="Control +2 매크로 ON")  # 밝은 노란색
                update_indicator(macro_ctrl2_indicator, False)

    elif number == '3':
        if force_off:
            if macro_ctrl3_running:
                macro_ctrl3_running = False
                log_message("Control +3 매크로 OFF")
                macro_ctrl3_btn.config(bg="#F5B7B1", text="Control +3 매크로 ON")
                update_indicator(macro_ctrl3_indicator, False)
        else:
            macro_ctrl3_running = not macro_ctrl3_running
            if macro_ctrl3_running:
                log_message("Control +3 매크로 ON")
                macro_ctrl3_btn.config(bg="#E74C3C", text="Control +3 매크로 OFF")  # 어두운 핑크색
                update_indicator(macro_ctrl3_indicator, True)
                threading.Thread(target=run_macro_ctrl3, daemon=True).start()
            else:
                log_message("Control +3 매크로 OFF")
                macro_ctrl3_btn.config(bg="#F5B7B1", text="Control +3 매크로 ON")  # 밝은 핑크색
                update_indicator(macro_ctrl3_indicator, False)

def run_macro_ctrl1():
    while macro_ctrl1_running:
        pyautogui.press('8')
        pyautogui.press('left')
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('8')
        pyautogui.press('left')
        pyautogui.press('enter')
        time.sleep(0.1)

def run_macro_ctrl2():
    while macro_ctrl2_running:
        pyautogui.press('7')
        pyautogui.press('left')
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('7')
        pyautogui.press('left')
        pyautogui.press('enter')
        time.sleep(0.1)

def run_macro_ctrl3():
    while macro_ctrl3_running:
        pyautogui.press('8')
        pyautogui.press('right')
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('8')
        pyautogui.press('right')
        pyautogui.press('enter')
        time.sleep(0.1)

# 키보드 입력에 따른 매크로 제어
def on_press(key):
    global pressed_keys
    pressed_keys.add(key)

    # Control 키 확인
    if keyboard.Key.ctrl in pressed_keys:
        try:
            if hasattr(key, 'char'):
                if key.char == '1' and '1' not in toggled_combinations:
                    toggle_macro_ctrl('1')
                    toggled_combinations.add('1')
                elif key.char == '2' and '2' not in toggled_combinations:
                    toggle_macro_ctrl('2')
                    toggled_combinations.add('2')
                elif key.char == '3' and '3' not in toggled_combinations:
                    toggle_macro_ctrl('3')
                    toggled_combinations.add('3')
        except AttributeError:
            pass
    else:
        try:
            if key.char == '[':   # '[' 키로 기본 매크로 ON/OFF
                toggle_macro()
            elif key.char == ']': # ']' 키로 7키 매크로 ON/OFF
                toggle_macro_7()
            elif key.char == '\\': # '\' 키로 8키 매크로 ON/OFF
                toggle_macro_8()
        except AttributeError:
            pass

def on_release(key):
    global pressed_keys
    pressed_keys.discard(key)
    # Remove toggled combinations when keys are released
    try:
        if key.char in ['1', '2', '3']:
            toggled_combinations.discard(key.char)
    except AttributeError:
        pass

# GUI 설정
root = tk.Tk()
root.title("매크로 제어")
root.geometry("500x900")  # 창 크기를 늘려서 새로운 버튼을 추가

# 기본 매크로 버튼과 상태 표시기
base_macro_frame = tk.Frame(root)
base_macro_frame.pack(pady=5)
base_macro_btn = tk.Button(base_macro_frame, text="기본 매크로 ON", command=toggle_macro, bg="#A9DFBF")  # 밝은 초록색
base_macro_btn.pack(side="left")
base_macro_indicator = tk.Canvas(base_macro_frame, width=20, height=20)
base_macro_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
base_macro_indicator.pack(side="right")

# 7키 전용 매크로 버튼과 상태 표시기
macro_7_frame = tk.Frame(root)
macro_7_frame.pack(pady=5)
macro_7_btn = tk.Button(macro_7_frame, text="7키 매크로 ON", command=toggle_macro_7, bg="#F1948A")  # 밝은 빨간색
macro_7_btn.pack(side="left")
macro_7_indicator = tk.Canvas(macro_7_frame, width=20, height=20)
macro_7_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
macro_7_indicator.pack(side="right")

# 8키 전용 매크로 버튼과 상태 표시기
macro_8_frame = tk.Frame(root)
macro_8_frame.pack(pady=5)
macro_8_btn = tk.Button(macro_8_frame, text="8키 매크로 ON", command=toggle_macro_8, bg="#85C1E9")  # 밝은 파란색
macro_8_btn.pack(side="left")
macro_8_indicator = tk.Canvas(macro_8_frame, width=20, height=20)
macro_8_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
macro_8_indicator.pack(side="right")

# Control +1 매크로 버튼과 상태 표시기
macro_ctrl1_frame = tk.Frame(root)
macro_ctrl1_frame.pack(pady=5)
macro_ctrl1_btn = tk.Button(macro_ctrl1_frame, text="Control +1 매크로 ON", command=lambda: toggle_macro_ctrl('1'), bg="#D7BDE2", state='disabled')  # 밝은 보라색
macro_ctrl1_btn.pack(side="left")
macro_ctrl1_indicator = tk.Canvas(macro_ctrl1_frame, width=20, height=20)
macro_ctrl1_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
macro_ctrl1_indicator.pack(side="right")

# Control +2 매크로 버튼과 상태 표시기
macro_ctrl2_frame = tk.Frame(root)
macro_ctrl2_frame.pack(pady=5)
macro_ctrl2_btn = tk.Button(macro_ctrl2_frame, text="Control +2 매크로 ON", command=lambda: toggle_macro_ctrl('2'), bg="#F9E79F", state='disabled')  # 밝은 노란색
macro_ctrl2_btn.pack(side="left")
macro_ctrl2_indicator = tk.Canvas(macro_ctrl2_frame, width=20, height=20)
macro_ctrl2_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
macro_ctrl2_indicator.pack(side="right")

# Control +3 매크로 버튼과 상태 표시기
macro_ctrl3_frame = tk.Frame(root)
macro_ctrl3_frame.pack(pady=5)
macro_ctrl3_btn = tk.Button(macro_ctrl3_frame, text="Control +3 매크로 ON", command=lambda: toggle_macro_ctrl('3'), bg="#F5B7B1", state='disabled')  # 밝은 핑크색
macro_ctrl3_btn.pack(side="left")
macro_ctrl3_indicator = tk.Canvas(macro_ctrl3_frame, width=20, height=20)
macro_ctrl3_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
macro_ctrl3_indicator.pack(side="right")

# 상태 표시 레이블
status_label = tk.Label(root, text="매크로 상태: OFF")
status_label.pack(pady=10)

# 로그 출력창 (스크롤이 가능한 Text 위젯)
log_text = ScrolledText(root, height=15, state='disabled', wrap=tk.WORD)
log_text.pack(fill=tk.BOTH, padx=10, pady=10)

# 키보드 리스너 설정
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

root.mainloop()
