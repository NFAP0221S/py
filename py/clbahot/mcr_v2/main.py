import tkinter as tk
import pyautogui
from pynput import keyboard
import json
import os
import threading
import time

class CircularButton(tk.Canvas):
    def __init__(self, master, radius=10, bg='red', command=None, **kwargs):
        super().__init__(master, width=2*radius, height=2*radius, highlightthickness=0, **kwargs)
        self.radius = radius
        self.bg = bg
        self.command = command
        self.circle = None
        self.draw_circle()
        self.bind("<Button-1>", self.on_click)

    def draw_circle(self):
        # 이미 그려진 원이 있다면 삭제
        if self.circle:
            self.delete(self.circle)
        self.circle = self.create_oval(2, 2, 2*self.radius, 2*self.radius, fill=self.bg, outline=self.bg)

    def update_color(self, new_color):
        self.bg = new_color
        self.draw_circle()

    def on_click(self, event):
        if self.command:
            self.command()

class ActionLow:
    def __init__(self, master, key='', description='', is_active=True, can_toggle=True):
        """
        can_toggle: 액션이 토글 가능한지 여부
        """
        self.frame = tk.Frame(master, borderwidth=1, relief=tk.RAISED)
        self.frame.pack(fill='x', padx=5, pady=2)

        self.key_input = tk.Entry(self.frame, width=10)
        self.key_input.insert(0, key)
        self.key_input.pack(side=tk.LEFT, padx=5)

        self.desc_input = tk.Entry(self.frame, width=30)
        self.desc_input.insert(0, description)
        self.desc_input.pack(side=tk.LEFT, padx=5)

        self.can_toggle = can_toggle
        if self.can_toggle:
            self.active_var = tk.BooleanVar(value=is_active)
            # 토글 가능한 원형 버튼
            self.active_button = CircularButton(
                self.frame, 
                radius=10, 
                bg='green' if is_active else 'red',
                command=self.toggle_active
            )
            self.active_button.pack(side=tk.RIGHT, padx=5)
        else:
            # 토글 불가능한 원형 버튼 (Action1)
            self.active_var = tk.BooleanVar(value=is_active)
            self.active_button = CircularButton(
                self.frame, 
                radius=10, 
                bg='green' if is_active else 'red',
                command=None  # 버튼 클릭 시 별도의 동작 없음
            )
            self.active_button.pack(side=tk.RIGHT, padx=5)

    def toggle_active(self):
        # 상태 토글
        new_state = not self.active_var.get()
        self.active_var.set(new_state)
        
        # 버튼 색상 변경
        new_color = 'green' if new_state else 'red'
        self.active_button.update_color(new_color)

class AutomationProgram:
    def __init__(self, root):
        self.root = root
        self.root.title("Automation Program")
        self.root.geometry("500x400")  # 창 크기 조절

        # 상단 프레임에 저장 버튼
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill='x', padx=10, pady=5)
        
        self.save_button = tk.Button(self.top_frame, text="Save", command=self.save_configurations)
        self.save_button.pack(side=tk.RIGHT)

        # 액션을 위한 프레임
        self.scrollable_frame = tk.Frame(self.root)
        self.scrollable_frame.pack(fill='both', expand=True)

        # 액션1: 토글 버튼 없음, 동작 시 활성화된 액션들만 중지 후 재활성화
        self.action1 = ActionLow(
            self.scrollable_frame, 
            key='-',  # Action1의 키 (예: 'a')
            description='잠시 정지', 
            is_active=True,
            can_toggle=False  # 버튼 없음
        )

        # 액션2: 토글 버튼 있음, 활성화 시 키 입력으로 'uuuu6' 실행
        self.action2 = ActionLow(
            self.scrollable_frame, 
            key='[',  # Action2의 키 (예: 's')
            description='혼마 왼쪽 무한돌리기', 
            is_active=True,
            can_toggle=True  # 토글 버튼 있음
        )

        # 액션3: 토글 버튼 있음, 활성화 시 키 입력으로 '77778' 실행
        self.action3 = ActionLow(
            self.scrollable_frame, 
            key=']',  # Action3의 키 (예: 'd')
            description='혼마 왼쪽 한번 돌리기', 
            is_active=True,  # 초기 상태 비활성화
            can_toggle=True  # 토글 버튼 있음
        )

        # 액션4: 토글 버튼 있음, 활성화 시 키 입력으로 '77778' 실행
        self.action4 = ActionLow(
            self.scrollable_frame, 
            key='`',  # Action3의 키 (예: 'd')
            description='자신 힐', 
            is_active=True,  # 초기 상태 비활성화
            can_toggle=True  # 토글 버튼 있음
        )

        # 액션5: 토글 버튼 있음, 활성화 시 키 입력으로 '77778' 실행
        self.action5 = ActionLow(
            self.scrollable_frame, 
            key='.',  # Action3의 키 (예: 'd')
            description='자신 보무', 
            is_active=True,  # 초기 상태 비활성화
            can_toggle=True  # 토글 버튼 있음
        )

        # 액션6: 토글 버튼 있음, 활성화 시 키 입력으로 '77778' 실행
        self.action6 = ActionLow(
            self.scrollable_frame, 
            key='=',  # Action3의 키 (예: 'd')
            description='탭탭 힐 보무', 
            is_active=True,  # 초기 상태 비활성화
            can_toggle=True  # 토글 버튼 있음
        )

         # 액션6: 토글 버튼 있음, 활성화 시 키 입력으로 '77778' 실행
        self.action7 = ActionLow(
            self.scrollable_frame, 
            key='\\',  # Action3의 키 (예: 'd')
            description='중독', 
            is_active=True,  # 초기 상태 비활성화
            can_toggle=True  # 토글 버튼 있음
        )

        # 관리할 액션 목록
        self.managed_actions = [self.action2, self.action3, self.action4, self.action5, self.action6, self.action7]

        # 중지를 위한 이벤트
        self.stop_event_action2 = threading.Event()
        self.stop_event_action3 = threading.Event()
        self.stop_event_action4 = threading.Event()
        self.stop_event_action5 = threading.Event()
        self.stop_event_action6 = threading.Event()
        self.stop_event_action7 = threading.Event()
        self.action2_thread = None  # Thread handle for Action2
        self.action3_thread = None  # Thread handle for Action3
        self.action4_thread = None  # Thread handle for Action4
        self.action5_thread = None  # Thread handle for Action4
        self.action6_thread = None  # Thread handle for Action4
        self.action7_thread = None  # Thread handle for Action4

        # 키 리스너 설정
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def save_configurations(self):
        configs = [
            {
                'key': self.action1.key_input.get(),
                'description': self.action1.desc_input.get(),
                'active': self.action1.active_var.get()
            },
            {
                'key': self.action2.key_input.get(),
                'description': self.action2.desc_input.get(),
                'active': self.action2.active_var.get()
            },
            {
                'key': self.action3.key_input.get(),
                'description': self.action3.desc_input.get(),
                'active': self.action3.active_var.get()
            },
            {
                'key': self.action4.key_input.get(),
                'description': self.action4.desc_input.get(),
                'active': self.action4.active_var.get()
            },
            {
                'key': self.action5.key_input.get(),
                'description': self.action5.desc_input.get(),
                'active': self.action5.active_var.get()
            },
            {
                'key': self.action6.key_input.get(),
                'description': self.action6.desc_input.get(),
                'active': self.action6.active_var.get()
            },
            {
                'key': self.action7.key_input.get(),
                'description': self.action7.desc_input.get(),
                'active': self.action7.active_var.get()
            }
        ]
        
        with open('automation_config.json', 'w') as f:
            json.dump(configs, f)
        print("Configurations saved!")

    def execute_action1(self):
        """
        Action1: Stop Active Actions Temporarily
        - 현재 활성화된 액션(Action2, Action3)을 중지하고 비활성화
        - 0.5초 후 중지된 액션들만 다시 활성화
        """
        if self.action1.active_var.get():
            print("Executing Action1: Stopping active actions temporarily.")
            
            # 중지할 액션들을 저장할 리스트
            self.active_actions_to_resume = []
            
            for action in self.managed_actions:
                if action.active_var.get():
                    self.active_actions_to_resume.append(action)
                    
                    # 중지 이벤트와 스레드 설정
                    if action == self.action2 and self.action2_thread and self.action2_thread.is_alive():
                        print("Stopping Action2's execution.")
                        self.stop_event_action2.set()
                        self.action2_thread.join()
                        self.stop_event_action2.clear()
                        # 액션 비활성화
                        action.active_var.set(False)
                        action.active_button.update_color('red')
                    
                    elif action == self.action3 and self.action3_thread and self.action3_thread.is_alive():
                        print("Stopping Action3's execution.")
                        self.stop_event_action3.set()
                        self.action3_thread.join()
                        self.stop_event_action3.clear()
                        # 액션 비활성화
                        action.active_var.set(False)
                        action.active_button.update_color('red')

                    elif action == self.action7 and self.action7_thread and self.action7_thread.is_alive():
                        print("Stopping Action3's execution.")
                        self.stop_event_action7.set()
                        self.action7_thread.join()
                        self.stop_event_action7.clear()
                        # 액션 비활성화
                        action.active_var.set(False)
                        action.active_button.update_color('red')
            
            # 0.5초 후 중지된 액션들만 다시 활성화
            self.root.after(500, self.resume_actions)

    def resume_actions(self):
        """
        중지된 액션들을 다시 활성화
        """
        for action in self.active_actions_to_resume:
            action.active_var.set(True)
            action.active_button.update_color('green')
            print(f"{action.desc_input.get()} is ready again.")
        
        # 리스트 초기화
        self.active_actions_to_resume = []

    def execute_action2(self):
        """
        Action2: 혼마 왼쪽 무한 돌리기
        """
        if self.action2.active_var.get():
            print("Executing Action2: 혼마 왼쪽 돌리기")
            try:
                pyautogui.press('esc')  # 키 누르기
                while True:
                    if self.stop_event_action2.is_set():
                        print("Action2 execution stopped.")
                        break
                    
                    # pyautogui.typewrite(['6', 'left', 'enter'], interval=0.02)
                    pyautogui.typewrite(['5', 'left', 'enter'], interval=0.02)
            except Exception as e:
                print(f"Error during Action2 execution: {e}")

    def execute_action3(self):
        """
        Action3: 혼마 왼쪽 한번 돌리기
        """
        if self.action3.active_var.get():
            print("Executing Action3: 77778")
            try:
                pyautogui.press('esc')  # 키 누르기
                pyautogui.typewrite(['7', 'left', 'enter'], interval=0.02)
                # time.sleep(0.01)
            except Exception as e:
                print(f"Error during Action3 execution: {e}")
            # try:
            #     pyautogui.press('esc')  # 키 누르기
            #     while True:
            #         if self.stop_event_action3.is_set():
            #             print("Action2 execution stopped.")
            #             break
                    
            #         # pyautogui.typewrite(['6', 'left', 'enter'], interval=0.02)
            #         pyautogui.typewrite(['7', 'left', 'enter'], interval=0.02)
            # except Exception as e:
            #     print(f"Error during Action2 execution: {e}")

    def execute_action4(self):
        """
        Action4: 자신 힐
        """
        if self.action3.active_var.get():
            print("Executing Action3: 77778")
            try:
                pyautogui.press('esc')  # 키 누르기
                pyautogui.typewrite(['1', 'home', 'enter', '1', 'enter'], interval=0.02)
                # time.sleep(0.01)
            except Exception as e:
                print(f"Error during Action3 execution: {e}")

    def execute_action5(self):
        """
        Action4: 자신 보무
        """
        if self.action3.active_var.get():
            print("Executing Action3: 77778")
            try:
                pyautogui.press('esc')  # 키 누르기
                pyautogui.typewrite(['9', 'home', 'enter', '0', 'enter'], interval=0.02)
                # time.sleep(0.01)
            except Exception as e:
                print(f"Error during Action3 execution: {e}")

    def execute_action6(self):
        """
        Action4: 탭탭 힐 보무
        """
        if self.action3.active_var.get():
            print("Executing Action3: 77778")
            try:
                pyautogui.press('tab')  # 키 누르기
                pyautogui.press('tab')  # 키 누르기
                pyautogui.typewrite(['1', '1', '9', '0'], interval=0.02)
                # time.sleep(0.01)
            except Exception as e:
                print(f"Error during Action3 execution: {e}")
    
    def execute_action7(self):
        """
        Action4: 탭탭 힐 보무
        """
        if self.action7.active_var.get():
            print("Executing Action7: 혼마 왼쪽 돌리기")
            try:
                pyautogui.press('esc')  # 키 누르기
                while True:
                    if self.stop_event_action7.is_set():
                        print("Action2 execution stopped.")
                        break
                    
                    # pyautogui.typewrite(['6', 'left', 'enter'], interval=0.02)
                    pyautogui.typewrite(['6', 'left', 'enter'], interval=0.02)
            except Exception as e:
                print(f"Error during Action2 execution: {e}")

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                pressed_key = key.char.lower()  # 대소문자 구분 없이 처리

                # Action1 키가 눌렸는지 확인
                if pressed_key == self.action1.key_input.get() and self.action1.active_var.get():
                    print("Action1 Key Pressed")
                    # Action1을 별도의 스레드에서 실행
                    action1_thread = threading.Thread(target=self.execute_action1)
                    action1_thread.start()

                # Action2 키가 눌렸는지 확인
                elif pressed_key == self.action2.key_input.get() and self.action2.active_var.get():
                    print("Action2 Key Pressed")
                    # Action2 실행 중인지 확인
                    if self.action2_thread and self.action2_thread.is_alive():
                        print("Action2 is already running.")
                    else:
                        # Action2를 별도의 스레드에서 실행
                        self.action2_thread = threading.Thread(target=self.execute_action2)
                        self.action2_thread.start()

                # Action3 키가 눌렸는지 확인
                elif pressed_key == self.action3.key_input.get() and self.action3.active_var.get():
                    print("Action3 Key Pressed")
                    # Action3 실행 중인지 확인
                    if self.action3_thread and self.action3_thread.is_alive():
                        print("Action3 is already running.")
                    else:
                        # Action3을 별도의 스레드에서 실행
                        self.action3_thread = threading.Thread(target=self.execute_action3)
                        self.action3_thread.start()

                # Action4 키가 눌렸는지 확인                        
                elif pressed_key == self.action4.key_input.get() and self.action4.active_var.get():
                    print("Action4 Key Pressed")
                    # Action4 실행 중인지 확인
                    if self.action4_thread and self.action4_thread.is_alive():
                        print("Action5 is already running.")
                    else:
                        # Action3을 별도의 스레드에서 실행
                        self.action4_thread = threading.Thread(target=self.execute_action4)
                        self.action4_thread.start()

                # Action6 키가 눌렸는지 확인                        
                elif pressed_key == self.action5.key_input.get() and self.action5.active_var.get():
                    print("Action5 Key Pressed")
                    # Action5 실행 중인지 확인
                    if self.action5_thread and self.action5_thread.is_alive():
                        print("Action5 is already running.")
                    else:
                        # Action5을 별도의 스레드에서 실행
                        self.action5_thread = threading.Thread(target=self.execute_action5)
                        self.action5_thread.start()

                # Action6 키가 눌렸는지 확인                        
                elif pressed_key == self.action6.key_input.get() and self.action6.active_var.get():
                    print("Action6 Key Pressed")
                    # Action4 실행 중인지 확인
                    if self.action6_thread and self.action6_thread.is_alive():
                        print("Action6 is already running.")
                    else:
                        # Action6을 별도의 스레드에서 실행
                        self.action6_thread = threading.Thread(target=self.execute_action6)
                        self.action6_thread.start()

                 # Action7 키가 눌렸는지 확인                        
                elif pressed_key == self.action7.key_input.get() and self.action7.active_var.get():
                    print("Action7 Key Pressed")
                    # Action4 실행 중인지 확인
                    if self.action7_thread and self.action7_thread.is_alive():
                        print("Action7 is already running.")
                    else:
                        # Action7을 별도의 스레드에서 실행
                        self.action7_thread = threading.Thread(target=self.execute_action7)
                        self.action7_thread.start()        
        except AttributeError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomationProgram(root)
    root.mainloop()
