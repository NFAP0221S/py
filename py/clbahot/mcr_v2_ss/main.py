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
            self.active_button = CircularButton(
                self.frame, 
                radius=10, 
                bg='green' if is_active else 'red',
                command=self.toggle_active
            )
            self.active_button.pack(side=tk.RIGHT, padx=5)
        else:
            self.active_var = tk.BooleanVar(value=is_active)
            self.active_button = CircularButton(
                self.frame, 
                radius=10, 
                bg='green' if is_active else 'red',
                command=None
            )
            self.active_button.pack(side=tk.RIGHT, padx=5)

    def toggle_active(self):
        new_state = not self.active_var.get()
        self.active_var.set(new_state)
        new_color = 'green' if new_state else 'red'
        self.active_button.update_color(new_color)

class AutomationProgram:
    def __init__(self, root):
        self.root = root
        self.root.title("Automation Program")
        self.root.geometry("500x400")

        # 방향키 상태 관리를 위한 변수 추가
        self.arrow_key_pressed = False

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill='x', padx=10, pady=5)
        
        self.save_button = tk.Button(self.top_frame, text="Save", command=self.save_configurations)
        self.save_button.pack(side=tk.RIGHT)

        self.scrollable_frame = tk.Frame(self.root)
        self.scrollable_frame.pack(fill='both', expand=True)

        # 액션1: 정지 버튼
        self.action1 = ActionLow(
            self.scrollable_frame, 
            key='-',
            description='잠시 정지', 
            is_active=True,
            can_toggle=False
        )

        # 액션2: 혼마 왼쪽 무한돌리기
        self.action2 = ActionLow(
            self.scrollable_frame, 
            key='[',
            description='혼마 왼쪽 무한돌리기', 
            is_active=True,
            can_toggle=True
        )

        # 액션3: 혼마 왼쪽 한번 돌리기
        self.action3 = ActionLow(
            self.scrollable_frame, 
            key=']',
            description='혼마 왼쪽 한번 돌리기', 
            is_active=True,
            can_toggle=True
        )

        # 액션4: 자신 힐
        self.action4 = ActionLow(
            self.scrollable_frame, 
            key='`',
            description='자신 힐', 
            is_active=True,
            can_toggle=True
        )

        # 액션5: 자신 보무
        self.action5 = ActionLow(
            self.scrollable_frame, 
            key='.',
            description='자신 보무', 
            is_active=True,
            can_toggle=True
        )

        # 액션6: 탭탭 힐 보무
        self.action6 = ActionLow(
            self.scrollable_frame, 
            key='=',
            description='탭탭 힐 보무', 
            is_active=True,
            can_toggle=True
        )

        # 액션7: 중독
        self.action7 = ActionLow(
            self.scrollable_frame, 
            key='\\',
            description='중독', 
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

        # Thread handles
        self.action2_thread = None
        self.action3_thread = None
        self.action4_thread = None
        self.action5_thread = None
        self.action6_thread = None
        self.action7_thread = None

        # 키 리스너 설정 (press와 release 모두 감지)
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()

    def save_configurations(self):
        configs = []
        for action in [self.action1] + self.managed_actions:
            configs.append({
                'key': action.key_input.get(),
                'description': action.desc_input.get(),
                'active': action.active_var.get()
            })
        
        with open('automation_config.json', 'w') as f:
            json.dump(configs, f)
        print("Configurations saved!")

    def execute_action1(self):
        """
        Action1: Stop Active Actions
        """
        if self.action1.active_var.get():
            print("Executing Action1: Stopping running actions.")
            
            # 실행 중인 스레드 확인 및 중지
            for thread, event in [
                (self.action2_thread, self.stop_event_action2),
                (self.action3_thread, self.stop_event_action3),
                (self.action7_thread, self.stop_event_action7)
            ]:
                if thread and thread.is_alive():
                    print(f"Stopping action execution.")
                    event.set()
                    thread.join(timeout=1)
                    event.clear()

    def execute_action2(self):
        """
        Action2: 혼마 왼쪽 무한 돌리기
        """
        if self.action2.active_var.get():
            print("Executing Action2: 혼마 왼쪽 돌리기")
            try:
                pyautogui.press('esc')
                while not self.stop_event_action2.is_set():
                    if not self.arrow_key_pressed:  # 방향키가 눌려있지 않을 때만
                        pyautogui.typewrite(['5', 'left', 'enter'], interval=0.02)
                    else:
                        time.sleep(0.1)  # 방향키가 눌려있는 동안 대기
                print("Action2 execution stopped.")
            except Exception as e:
                print(f"Error during Action2 execution: {e}")

    def execute_action3(self):
        """
        Action3: 혼마 왼쪽 한번 돌리기
        """
        if self.action3.active_var.get():
            try:
                pyautogui.press('esc')
                pyautogui.typewrite(['7', 'left', 'enter'], interval=0.02)
            except Exception as e:
                print(f"Error during Action3 execution: {e}")

    def execute_action4(self):
        """
        Action4: 자신 힐
        """
        if self.action4.active_var.get():
            try:
                pyautogui.press('esc')
                pyautogui.typewrite(['1', 'home', 'enter', '1', 'enter'], interval=0.02)
            except Exception as e:
                print(f"Error during Action4 execution: {e}")

    def execute_action5(self):
        """
        Action5: 자신 보무
        """
        if self.action5.active_var.get():
            try:
                pyautogui.press('esc')
                pyautogui.typewrite(['9', 'home', 'enter', '0', 'enter'], interval=0.02)
            except Exception as e:
                print(f"Error during Action5 execution: {e}")

    def execute_action6(self):
        """
        Action6: 탭탭 힐 보무
        """
        if self.action6.active_var.get():
            try:
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.typewrite(['1', '1', '9', '0'], interval=0.02)
            except Exception as e:
                print(f"Error during Action6 execution: {e}")
    
    def execute_action7(self):
        """
        Action7: 중독
        """
        if self.action7.active_var.get():
            try:
                pyautogui.press('esc')
                while not self.stop_event_action7.is_set():
                    if not self.arrow_key_pressed:  # 방향키가 눌려있지 않을 때만
                        pyautogui.typewrite(['7', 'left', 'enter'], interval=0.02)
                    else:
                        time.sleep(0.1)  # 방향키가 눌려있는 동안 대기
                print("Action7 execution stopped.")
            except Exception as e:
                print(f"Error during Action7 execution: {e}")

    def on_release(self, key):
        """
        키가 떼어졌을 때의 처리
        """
        try:
            # 방향키가 떼어졌을 때
            if hasattr(key, 'name') and key.name in ['up', 'down', 'left', 'right']:
                self.arrow_key_pressed = False
                print("Arrow key released - resuming actions")
        except AttributeError:
            pass

    def on_press(self, key):
        """
        키가 눌렸을 때의 처리
        """
        try:
            # 방향키 감지
            if hasattr(key, 'name') and key.name in ['up', 'down', 'left', 'right']:
                self.arrow_key_pressed = True
                print("Arrow key pressed - pausing actions")
                return

            if hasattr(key, 'char') and key.char is not None:
                pressed_key = key.char.lower()

                # Action1 (정지) 키 처리
                if pressed_key == self.action1.key_input.get() and self.action1.active_var.get():
                    print("Action1 Key Pressed")
                    action1_thread = threading.Thread(target=self.execute_action1)
                    action1_thread.start()
                    return

                # 액션 실행 매핑
                action_mapping = {
                    self.action2: (self.action2_thread, self.execute_action2),
                    self.action3: (self.action3_thread, self.execute_action3),
                    self.action4: (self.action4_thread, self.execute_action4),
                    self.action5: (self.action5_thread, self.execute_action5),
                    self.action6: (self.action6_thread, self.execute_action6),
                    self.action7: (self.action7_thread, self.execute_action7),
                }

                # 각 액션 키 처리
                for action, (thread_var, execute_func) in action_mapping.items():
                    if pressed_key == action.key_input.get() and action.active_var.get():
                        print(f"{action.desc_input.get()} Key Pressed")
                        if not (thread_var and thread_var and thread_var.is_alive()):
                            new_thread = threading.Thread(target=execute_func)
                            setattr(self, f"action{list(action_mapping.keys()).index(action) + 2}_thread", new_thread)
                            new_thread.start()
                        return

        except AttributeError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomationProgram(root)
    root.mainloop()