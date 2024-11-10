import tkinter as tk
import pyautogui
import time
import threading
from tkinter.scrolledtext import ScrolledText

# 매크로 상태를 저장하는 변수
macro_running = False
macro_7_running = False
macro_8_running = False
macro_paused = False
log_index = 1  # 로그 인덱스 초기화

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
    indicator.itemconfig(indicator_circle, fill=color)

# 매크로 실행 및 중지를 위한 함수
def toggle_macro():
    global macro_running, macro_7_running, macro_8_running

    macro_running = not macro_running
    if macro_running:
        log_message("기본 매크로 ON")
        base_macro_btn.config(bg="#4D4D4D", text="기본 매크로 OFF")  # 어두운 회색
        update_indicator(base_macro_indicator, True)
    else:
        # 기본 매크로가 OFF되면 모든 매크로 OFF
        macro_running = False
        macro_7_running = False
        macro_8_running = False
        log_message("기본 매크로 OFF")
        base_macro_btn.config(bg="#A9DFBF", text="기본 매크로 ON")  # 밝은 초록색
        update_indicator(base_macro_indicator, False)
        
        # 7키와 8키 매크로도 OFF 상태로 전환
        macro_7_btn.config(bg="#F1948A", text="7키 매크로 ON")  # 밝은 빨간색
        update_indicator(macro_7_indicator, False)
        macro_8_btn.config(bg="#85C1E9", text="8키 매크로 ON")  # 밝은 파란색
        update_indicator(macro_8_indicator, False)

# 토글 매크로 8
def toggle_macro_8():
    global macro_8_running
    if macro_running:  # 기본 매크로가 켜진 상태에서만 8키 매크로 ON/OFF 가능
        macro_8_running = not macro_8_running
        if macro_8_running:
            log_message("8키 전용 매크로 ON")
            macro_8_btn.config(bg="#5DADE2", text="8키 매크로 OFF")  # 어두운 파란색
            update_indicator(macro_8_indicator, True)
            threading.Thread(target=run_macro_8).start()
        else:
            log_message("8키 전용 매크로 OFF")
            macro_8_btn.config(bg="#85C1E9", text="8키 매크로 ON")  # 밝은 파란색
            update_indicator(macro_8_indicator, False)

def run_macro_8():
    while macro_8_running and not macro_paused:
        pyautogui.press('8')
        pyautogui.press('enter')
        # time.sleep(0.1)

# 토글 매크로 7
def toggle_macro_7():
    global macro_7_running
    if macro_running:  # 기본 매크로가 켜진 상태에서만 7키 매크로 ON/OFF 가능
        macro_7_running = not macro_7_running
        if macro_7_running:
            log_message("7키 전용 매크로 ON")
            macro_7_btn.config(bg="#CD6155", text="7키 매크로 OFF")  # 어두운 빨간색
            update_indicator(macro_7_indicator, True)
            threading.Thread(target=run_macro_7).start()
        else:
            log_message("7키 전용 매크로 OFF")
            macro_7_btn.config(bg="#F1948A", text="7키 매크로 ON")  # 밝은 빨간색
            update_indicator(macro_7_indicator, False)

def run_macro_7():
    while macro_7_running and not macro_paused:
        pyautogui.press('7')
        pyautogui.press('enter')
        time.sleep(0.1)

# GUI 설정
root = tk.Tk()
root.title("매크로 제어")
root.geometry("400x500")

# 기본 매크로 버튼과 상태 표시기
base_macro_frame = tk.Frame(root)
base_macro_frame.pack(pady=5)
base_macro_btn = tk.Button(base_macro_frame, text="기본 매크로 ON", command=toggle_macro, bg="#A9DFBF")  # 밝은 초록색
base_macro_btn.pack(side="left")
base_macro_indicator = tk.Canvas(base_macro_frame, width=20, height=20)
indicator_circle = base_macro_indicator.create_oval(5, 5, 15, 15, fill="red")
base_macro_indicator.pack(side="right")

# 7키 전용 매크로 버튼과 상태 표시기
macro_7_frame = tk.Frame(root)
macro_7_frame.pack(pady=5)
macro_7_btn = tk.Button(macro_7_frame, text="7키 매크로 ON", command=toggle_macro_7, bg="#F1948A")  # 밝은 빨간색
macro_7_btn.pack(side="left")
macro_7_indicator = tk.Canvas(macro_7_frame, width=20, height=20)
macro_7_indicator.create_oval(5, 5, 15, 15, fill="red")
macro_7_indicator.pack(side="right")

# 8키 전용 매크로 버튼과 상태 표시기
macro_8_frame = tk.Frame(root)
macro_8_frame.pack(pady=5)
macro_8_btn = tk.Button(macro_8_frame, text="8키 매크로 ON", command=toggle_macro_8, bg="#85C1E9")  # 밝은 파란색
macro_8_btn.pack(side="left")
macro_8_indicator = tk.Canvas(macro_8_frame, width=20, height=20)
macro_8_indicator.create_oval(5, 5, 15, 15, fill="red")
macro_8_indicator.pack(side="right")

# 상태 표시 레이블
status_label = tk.Label(root, text="매크로 상태: OFF")
status_label.pack(pady=10)

# 로그 출력창 (스크롤이 가능한 Text 위젯)
log_text = ScrolledText(root, height=10, state='disabled', wrap=tk.WORD)
log_text.pack(fill=tk.BOTH, padx=10, pady=10)

root.mainloop()
