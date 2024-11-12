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

    if exclude != '7':
        if macro_7_running:
            toggle_macro_7(force_off=True)
    if exclude != '8':
        if macro_8_running:
            toggle_macro_8(force_off=True)

# 기본 매크로 ON/OFF 토글 함수
def toggle_macro():
    global macro_running, macro_7_running, macro_8_running

    macro_running = not macro_running
    if macro_running:
        log_message("기본 매크로 ON")
        base_macro_btn.config(bg="#4D4D4D", text="기본 매크로 OFF")  # 어두운 회색
        update_indicator(base_macro_indicator, True)
        
        # 7키, 8키, Q 매크로 버튼 활성화
        macro_7_btn.config(state='normal')
        macro_8_btn.config(state='normal')
        macro_q_btn.config(state='normal')
    else:
        # 기본 매크로가 OFF되면 모든 매크로 OFF
        macro_running = False
        macro_7_running = False
        macro_8_running = False
        log_message("기본 매크로 OFF")
        base_macro_btn.config(bg="#A9DFBF", text="기본 매크로 ON")  # 밝은 초록색
        update_indicator(base_macro_indicator, False)
        
        # 7키와 8키 매크로도 OFF 상태로 전환
        macro_7_btn.config(bg="#F1948A", text="7키 매크로 ON", state='disabled')  # 밝은 빨간색
        update_indicator(macro_7_indicator, False)
        macro_8_btn.config(bg="#85C1E9", text="8키 매크로 ON", state='disabled')  # 밝은 파란색
        update_indicator(macro_8_indicator, False)
        macro_q_btn.config(state='disabled')  # Q 매크로 버튼 비활성화

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
        pyautogui.press('8')
        pyautogui.press('enter')
        pyautogui.press('8')
        pyautogui.press('enter')
        pyautogui.press('8')
        pyautogui.press('enter')
        pyautogui.press('8')
        pyautogui.press('enter')

# Q 매크로 실행 함수 (일회성)
def do_macro_q():
    if not macro_running:
        log_message("기본 매크로가 꺼져 있어 Q 매크로를 사용할 수 없습니다.")
        return
    log_message("Q 매크로 실행: 8 키 입력")
    pyautogui.press('8')
    # 추가로 'enter' 키가 필요하면 아래 주석을 해제하세요
    # pyautogui.press('enter')

# 키보드 입력에 따른 매크로 제어
def on_press(key):
    global pressed_keys
    pressed_keys.add(key)

    try:
        if key.char == '[':   # '[' 키로 기본 매크로 ON/OFF
            toggle_macro()
        elif key.char == ']': # ']' 키로 7키 매크로 ON/OFF
            toggle_macro_7()
        elif key.char == 'q': # 'q' 키로 Q 매크로 실행
            do_macro_q()
    except AttributeError:
        pass

def on_release(key):
    global pressed_keys
    pressed_keys.discard(key)
    # Remove toggled combinations when keys are released
    try:
        if key.char in ['q', '[', ']']:
            toggled_combinations.discard(key.char)
    except AttributeError:
        pass

# GUI 설정
root = tk.Tk()
root.title("매크로 제어")
root.geometry("500x700")  # 창 크기를 조정

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
macro_7_btn = tk.Button(macro_7_frame, text="7키 매크로 ON", command=toggle_macro_7, bg="#F1948A", state='disabled')  # 밝은 빨간색
macro_7_btn.pack(side="left")
macro_7_indicator = tk.Canvas(macro_7_frame, width=20, height=20)
macro_7_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
macro_7_indicator.pack(side="right")

# 8키 전용 매크로 버튼과 상태 표시기
macro_8_frame = tk.Frame(root)
macro_8_frame.pack(pady=5)
macro_8_btn = tk.Button(macro_8_frame, text="8키 매크로 ON", command=toggle_macro_8, bg="#85C1E9", state='disabled')  # 밝은 파란색
macro_8_btn.pack(side="left")
macro_8_indicator = tk.Canvas(macro_8_frame, width=20, height=20)
macro_8_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
macro_8_indicator.pack(side="right")

# Q 매크로 버튼 (일회성 실행)
macro_q_frame = tk.Frame(root)
macro_q_frame.pack(pady=5)
macro_q_btn = tk.Button(macro_q_frame, text="Q 매크로 실행", command=do_macro_q, bg="#AED6F1", state='disabled')  # 밝은 파란색
macro_q_btn.pack(side="left")
macro_q_indicator = tk.Canvas(macro_q_frame, width=20, height=20)
macro_q_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
macro_q_indicator.pack(side="right")

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
