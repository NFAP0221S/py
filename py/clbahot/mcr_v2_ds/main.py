import tkinter as tk
import pyautogui
from pynput import keyboard
import json
import random
import threading
import time
import platform

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

        # 운영체제 확인 및 interval 설정
        system = platform.system()
        self.type_008_interval = 0.08 if system == 'Windows' else 0.02
        self.type_002_interval = 0.02 if system == 'Windows' else 0.005

        # 방향키 상태를 추적하기 위한 변수 추가
        self.direction_key_pressed = False

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
            key='-',
            description='잠시 정지', 
            is_active=True,
            can_toggle=False
        )

        # 액션2: 토글 버튼 있음
        self.action2 = ActionLow(
            self.scrollable_frame, 
            key='[',
            description='혼마 왼쪽 무한돌리기', 
            is_active=True,
            can_toggle=True
        )

        # 액션3: 토글 버튼 있음
        self.action3 = ActionLow(
            self.scrollable_frame, 
            key=']',
            description='혼마 왼쪽 한번 돌리기', 
            is_active=True,
            can_toggle=True
        )

        # 액션4: 토글 버튼 있음
        self.action4 = ActionLow(
            self.scrollable_frame, 
            key='`',
            description='자신 힐', 
            is_active=True,
            can_toggle=True
        )

        # 액션5: 토글 버튼 있음
        self.action5 = ActionLow(
            self.scrollable_frame, 
            key='2',
            description='힐', 
            is_active=True,
            can_toggle=True
        )

        # 액션6: 토글 버튼 있음
        self.action6 = ActionLow(
            self.scrollable_frame, 
            key='=',
            description='나 보무 너 보무', 
            is_active=True,
            can_toggle=True
        )

        # 액션7: 토글 버튼 있음
        self.action7 = ActionLow(
            self.scrollable_frame, 
            # key='\\',
            key='1',
            description='힐', 
            is_active=True,
            can_toggle=True
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
        self.action2_thread = None
        self.action3_thread = None
        self.action4_thread = None
        self.action5_thread = None
        self.action6_thread = None
        self.action7_thread = None

        # 키보드 리스너 설정 (press와 release 모두 감지)
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
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
        Action1: Stop Active Actions
        - 현재 실행 중인 액션들을 중지
        - active 상태는 유지
        """
        if self.action1.active_var.get():
            print("Executing Action1: Stopping running actions.")
            
            # 먼저 모든 stop 이벤트를 설정
            self.stop_event_action2.set()
            self.stop_event_action3.set()
            self.stop_event_action5.set()
            self.stop_event_action7.set()
            
            # 실행 중인 스레드 확인 및 중지
            if self.action2_thread and self.action2_thread.is_alive():
                print("Stopping Action2's execution.")
                self.action2_thread.join(timeout=1.0)
                
            if self.action3_thread and self.action3_thread.is_alive():
                print("Stopping Action3's execution.")
                self.action3_thread.join(timeout=1.0)

            if self.action5_thread and self.action5_thread.is_alive():  # Action5 추가
                print("Stopping Action5's execution.")
                self.action5_thread.join(timeout=1.0)
                
            if self.action7_thread and self.action7_thread.is_alive():
                print("Stopping Action7's execution.")
                self.action7_thread.join(timeout=1.0)

            # 모든 스레드가 종료된 후에 이벤트 초기화
            self.stop_event_action2.clear()
            self.stop_event_action3.clear()
            self.stop_event_action5.clear()  
            self.stop_event_action7.clear()

            # 스레드 핸들 초기화
            self.action2_thread = None
            self.action3_thread = None
            self.action5_thread = None
            self.action7_thread = None

    def execute_action2(self):
        """
        Action2: 혼마 왼쪽 무한 돌리기
        """
        if self.action2.active_var.get():
            print("Executing Action2: 혼마 왼쪽 돌리기")
            try:
                pyautogui.press('esc')
                while True:
                    if self.stop_event_action2.is_set():
                        print("Action2 execution stopped.")
                        break
                    
                    # 방향키가 눌려있지 않을 때만 실행
                    if not self.direction_key_pressed:
                        pyautogui.typewrite(['6', 'left', 'enter'], self.type_002_interval)
                        # pyautogui.typewrite(['9', 'left', 'enter', '0', 'enter'], self.type_008_interval)
                    else:
                        # 방향키가 눌려있는 동안은 잠시 대기
                        time.sleep(0.01)
                        
            except Exception as e:
                print(f"Error during Action2 execution: {e}")

    def execute_action3(self):
        """
        Action3: 혼마 왼쪽 한번 돌리기
        """
        if self.action3.active_var.get():
            print("Executing Action3: 77778")
            try:
                pyautogui.press('esc')
                pyautogui.typewrite(['6', 'left', 'enter'], self.type_002_interval)
            except Exception as e:
                print(f"Error during Action3 execution: {e}")

    def execute_action4(self):
        """
        Action4: 자신 힐
        """
        if self.action3.active_var.get():
            print("Executing Action4: 자신 힐")
            try:
                pyautogui.press('esc')
                pyautogui.typewrite(['1', 'home', 'enter', '1', 'enter'], self.type_008_interval)
            except Exception as e:
                print(f"Error during Action4 execution: {e}")

    # def execute_action5(self):
    #     """
    #     Action5: 힐
    #     """
        # if self.action3.active_var.get():
        #     print("Executing Action5: 힐")
        #     try:
        #         #6, 7 중에서 랜덤하게 횟수 선택
        #         press_count = random.randint(3, 4)
        #         print(f"Pressing '1' {press_count} times")
                
        #         # 선택된 횟수만큼 '1' 키 입력
        #         for _ in range(press_count):
        #             pyautogui.press('1')
        #             # time.sleep(0.02)  # 너무 빠른 입력 방지
        #         # pyautogui.press('1')
        #         # pyautogui.press('1')
        #         # pyautogui.press('1')
        #         pyautogui.press('4')
        #     except Exception as e:
        #         print(f"Error during Action5 execution: {e}")

    def execute_action5(self):
        """
        Action5: 연속 힐
        """
        if self.action5.active_var.get():
            print("Executing Action5: 연속 힐")
            try:
                while True:
                    if self.stop_event_action5.is_set():  # set() 대신 is_set() 사용
                        print("Action5 execution stopped.")
                        break
                    
                    if not self.direction_key_pressed:
                        pyautogui.typewrite(['1', '1', '4'], self.type_002_interval)
                    else:
                        time.sleep(0.01)
                        
            except Exception as e:
                print(f"Error during Action5 execution: {e}")

    def execute_action6(self):
        """
        Action6: 탭탭 힐 보무
        """
        if self.action3.active_var.get():
            print("Executing Action6: 탭탭 힐 보무")
            try:
                pyautogui.press('esc')
                pyautogui.typewrite(['9', 'home', 'enter', '0', 'enter'], self.type_008_interval)
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.typewrite(['9','0','1'], self.type_002_interval)
            except Exception as e:
                print(f"Error during Action6 execution: {e}")
    
    def execute_action7(self):
        """
        Action7: 단체보무
        """
        # if self.action2.active_var.get():
            # print("Executing Action2: 혼마 왼쪽 돌리기")
            # try:
                # pyautogui.press('4')
                # pyautogui.press('esc')
                # while True:
                #     if self.stop_event_action2.is_set():
                #         print("Action2 execution stopped.")
                #         break
                    
                #     # 방향키가 눌려있지 않을 때만 실행
                #     if not self.direction_key_pressed:
                #         pyautogui.typewrite(['9', 'left', 'enter', '0', 'enter'], self.type_008_interval)
                #     else:
                #         time.sleep(0.01)
                        
            # except Exception as e:
                # print(f"Error during Action2 execution: {e}")

    def on_press(self, key):
        try:
            # 방향키 감지
            if key == keyboard.Key.left or key == keyboard.Key.right or key == keyboard.Key.up or key == keyboard.Key.down:
                self.direction_key_pressed = True
                
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
                        print("Action4 is already running.")
                    else:
                        # Action4를 별도의 스레드에서 실행
                        self.action4_thread = threading.Thread(target=self.execute_action4)
                        self.action4_thread.start()

                # Action5 키가 눌렸는지 확인                        
                elif pressed_key == self.action5.key_input.get() and self.action5.active_var.get():
                    print("Action5 Key Pressed")
                    # Action5 실행 중인지 확인
                    if self.action5_thread and self.action5_thread.is_alive():
                        print("Action5 is already running.")
                    else:
                        # Action5를 별도의 스레드에서 실행
                        self.action5_thread = threading.Thread(target=self.execute_action5)
                        self.action5_thread.start()

                # Action6 키가 눌렸는지 확인                        
                elif pressed_key == self.action6.key_input.get() and self.action6.active_var.get():
                    print("Action6 Key Pressed")
                    # Action6 실행 중인지 확인
                    if self.action6_thread and self.action6_thread.is_alive():
                        print("Action6 is already running.")
                    else:
                        # Action6을 별도의 스레드에서 실행
                        self.action6_thread = threading.Thread(target=self.execute_action6)
                        self.action6_thread.start()

                # Action7 키가 눌렸는지 확인                        
                elif pressed_key == self.action7.key_input.get() and self.action7.active_var.get():
                    print("Action7 Key Pressed")
                    # Action7 실행 중인지 확인
                    if self.action7_thread and self.action7_thread.is_alive():
                        print("Action7 is already running.")
                    else:
                        # Action7을 별도의 스레드에서 실행
                        self.action7_thread = threading.Thread(target=self.execute_action7)
                        self.action7_thread.start()        
        except AttributeError:
            pass

    def on_release(self, key):
        # 방향키 release 감지
        if key == keyboard.Key.left or key == keyboard.Key.right or key == keyboard.Key.up or key == keyboard.Key.down:
            self.direction_key_pressed = False

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomationProgram(root)
    root.mainloop()