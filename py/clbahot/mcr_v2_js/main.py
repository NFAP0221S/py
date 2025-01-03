import tkinter as tk
import pyautogui
from pynput import keyboard, mouse
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

        # 키보드와 마우스 리스너 설정
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener.start()
        self.mouse_listener.start()

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
            key='3',  # Action2의 키 (예: 's')
            description='투평', 
            is_active=True,
            can_toggle=True  # 토글 버튼 있음
        )

        # 액션3: 626초마다 6,7,8 입력
        self.action3 = ActionLow(
            self.scrollable_frame, 
            key='[',
            description='626초마다 678입력', 
            is_active=True,
            can_toggle=True
        )

        # 액션4: 376초마다 9 입력
        self.action4 = ActionLow(
            self.scrollable_frame, 
            key=']',
            description='376초마다 9입력', 
            is_active=True,
            can_toggle=True
        )

        # 액션5: 186초마다 0 입력
        self.action5 = ActionLow(
            self.scrollable_frame, 
            key='\\',
            description='186초마다 0입력', 
            is_active=True,
            can_toggle=True
        )

        # 액션6: u4 입력
        self.action6 = ActionLow(
            self.scrollable_frame, 
            key='/',
            description='u4 입력', 
            is_active=True,
            can_toggle=True
        )

        # 액션7: 옵션+8 입력 추가
        self.action7 = ActionLow(
            self.scrollable_frame, 
            key='-',
            description='옵션+8 입력', 
            is_active=True,
            can_toggle=True
        )

        self.action8 = ActionLow(
            self.scrollable_frame, 
            key='left',  # 마우스 왼쪽 버튼
            description='좌클릭시 , 입력', 
            is_active=False,
            can_toggle=True
        )

        # 관리할 액션 목록 업데이트
        self.managed_actions = [self.action2, self.action3, self.action4, self.action5, self.action6, self.action7, self.action8 ]

        # 중지를 위한 이벤트
        self.stop_event_action2 = threading.Event()
        self.stop_event_action3 = threading.Event()
        self.stop_event_action4 = threading.Event()
        self.stop_event_action5 = threading.Event()
        self.stop_event_action6 = threading.Event()
        self.stop_event_action7 = threading.Event()
        self.stop_event_action8 = threading.Event()
        self.action2_thread = None  # Thread handle for Action2
        self.action3_thread = None  # Thread handle for Action3
        self.action4_thread = None  # Thread handle for Action4
        self.action5_thread = None  # Thread handle for Action4
        self.action6_thread = None  # Thread handle for Action4
        self.action7_thread = None  # Thread handle for Action4
        self.action8_thread = None

        # 키 리스너 설정
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:  # 왼쪽 버튼이 눌렸을 때
            if self.action8.active_var.get():
                print("Action8: Left Click Detected")
                # Action8을 별도의 스레드에서 실행
                if not (self.action8_thread and self.action8_thread.is_alive()):
                    self.action8_thread = threading.Thread(target=self.execute_action8)
                    self.action8_thread.start()

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
            },
            {
                'key': self.action8.key_input.get(),
                'description': self.action8.desc_input.get(),
                'active': self.action8.active_var.get()
            }
        ]
        
        with open('automation_config.json', 'w') as f:
            json.dump(configs, f)
        print("Configurations saved!")

    def execute_action1(self):
        """
        Action1: Stop Active Actions
        - 현재 실행 중인 액션들을 중지
        - active 상태는 유지
        """
        if self.action1.active_var.get():
            print("Executing Action1: Stopping running actions.")
            
            # 실행 중인 스레드 확인 및 중지
            if self.action2_thread and self.action2_thread.is_alive():
                print("Stopping Action2's execution.")
                self.stop_event_action2.set()
                self.action2_thread.join()
                self.stop_event_action2.clear()
                
            if self.action3_thread and self.action3_thread.is_alive():
                print("Stopping Action3's execution.")
                self.stop_event_action3.set()
                self.action3_thread.join()
                self.stop_event_action3.clear()

            if self.action6_thread and self.action6_thread.is_alive():
                print("Stopping Action6's execution.")
                self.stop_event_action6.set()
                self.action6_thread.join()
                self.stop_event_action6.clear()
                
            if self.action7_thread and self.action7_thread.is_alive():
                print("Stopping Action7's execution.")
                self.stop_event_action7.set()
                self.action7_thread.join()
                self.stop_event_action7.clear()

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
        Action2: 평
        """
        # if self.action2.active_var.get():
        #     print("Executing Action6: u4 input")
        #     try:
        #         # pyautogui.press('a')
        #         # pyautogui.press('3')
        #         pyautogui.typewrite(['u', 'a', 'u', 'a'], interval=0.02)
        #     except Exception as e:
        #         print(f"Error during Action6 execution: {e}")

        if self.action2.active_var.get():
            print("Executing Action2: Control + a press")
            try:
                keyboard_controller = keyboard.Controller()
                with keyboard_controller.pressed(keyboard.Key.ctrl):  # ctrl 키를 누른 상태 유지
                    keyboard_controller.press('a')  # a 키를 누름
                    time.sleep(0.5)  # 0.5초 대기
                    keyboard_controller.release('a')  # a 키를 뗌
            except Exception as e:
                print(f"Error during Action2 execution: {e}")

    def execute_action3(self):
        """
        Action3: 626초마다 6,7,8 입력
        """
        # if self.action3.active_var.get():
        #     print("Executing Action3: Periodic 6,7,8 input")
        #     try:
        #         last_time = 0
        #         while not self.stop_event_action3.is_set():
        #             current_time = time.time()
        #             if current_time - last_time >= 626:
        #                 pyautogui.typewrite(['6', '7', '8'], interval=0.02)
        #                 last_time = current_time
        #                 print("Executed 6,7,8 sequence")
        #             time.sleep(0.1)
        #     except Exception as e:
        #         print(f"Error during Action3 execution: {e}")

    def execute_action4(self):
        """
        Action4: 376초마다 9 입력
        """
        # if self.action4.active_var.get():
        #     print("Executing Action4: Periodic 9 input")
        #     try:
        #         last_time = 0
        #         while not self.stop_event_action4.is_set():
        #             current_time = time.time()
        #             if current_time - last_time >= 376:
        #                 pyautogui.press('9')
        #                 last_time = current_time
        #                 print("Executed 9")
        #             time.sleep(0.1)
        #     except Exception as e:
        #         print(f"Error during Action4 execution: {e}")

    def execute_action5(self):
        """
        Action5: 186초마다 0 입력
        """
        # if self.action5.active_var.get():
        #     print("Executing Action5: Periodic 0 input")
        #     try:
        #         last_time = 0
        #         while not self.stop_event_action5.is_set():
        #             current_time = time.time()
        #             if current_time - last_time >= 186:
        #                 pyautogui.press('0')
        #                 last_time = current_time
        #                 print("Executed 0")
        #             time.sleep(0.1)
        #     except Exception as e:
        #         print(f"Error during Action5 execution: {e}")

    def execute_action6(self):
        """
        Action6: 무한 평타
        """
        if self.action6.active_var.get():
            print("Executing Action6: 무한 평타")
            try:
                while True:
                    if self.stop_event_action6.is_set():
                        print("Action6 execution stopped.")
                        break
                    pyautogui.typewrite(['a'], interval=0.002)
            except Exception as e:
                print(f"Error during Action6 execution: {e}")

    def execute_action7(self):
        """
        Action7: 옵션+8 입력
        """
        # if self.action7.active_var.get():
        #     print("Executing Action7: Option+8 input")
        #     try:
        #         with pyautogui.hold('option'):
        #             pyautogui.press('8')
        #     except Exception as e:
        #         print(f"Error during Action7 execution: {e}")

    def execute_action8(self):
        """
        Action8: 좌클릭 시 , 입력
        """
        if self.action8.active_var.get():
            print("Executing Action8: , input")
            try:
                pyautogui.press(',')
            except Exception as e:
                print(f"Error during Action8 execution: {e}")    



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
