# gui/main_gui.py

import tkinter as tk
from utils.indicators import update_indicator

class MainGUI:
    def __init__(self, root, logger):
        self.root = root
        self.logger = logger
        self.macros = {}
        
        # GUI 컴포넌트 생성
        self.create_widgets()
        
    def create_widgets(self):
        # 기본 매크로 버튼과 상태 표시기
        self.base_macro_frame = tk.Frame(self.root)
        self.base_macro_frame.pack(pady=5)
        self.base_macro_btn = tk.Button(
            self.base_macro_frame, 
            text="기본 매크로 ON", 
            command=self.toggle_base_macro, 
            bg="#A9DFBF"  # 밝은 초록색
        )
        self.base_macro_btn.pack(side="left")
        self.base_macro_indicator = tk.Canvas(self.base_macro_frame, width=20, height=20)
        self.base_macro_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
        self.base_macro_indicator.pack(side="right")
        
        # 7키 전용 매크로 버튼과 상태 표시기
        self.macro_7_frame = tk.Frame(self.root)
        self.macro_7_frame.pack(pady=5)
        self.macro_7_btn = tk.Button(
            self.macro_7_frame, 
            text="7키 매크로 ON", 
            command=self.toggle_macro_7, 
            bg="#F1948A", 
            state='disabled'  # 기본 매크로가 꺼졌을 때 비활성화
        )
        self.macro_7_btn.pack(side="left")
        self.macro_7_indicator = tk.Canvas(self.macro_7_frame, width=20, height=20)
        self.macro_7_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
        self.macro_7_indicator.pack(side="right")
        
        # 8키 전용 매크로 버튼과 상태 표시기
        self.macro_8_frame = tk.Frame(self.root)
        self.macro_8_frame.pack(pady=5)
        self.macro_8_btn = tk.Button(
            self.macro_8_frame, 
            text="8키 매크로 ON", 
            command=self.toggle_macro_8, 
            bg="#85C1E9", 
            state='disabled'  # 기본 매크로가 꺼졌을 때 비활성화
        )
        self.macro_8_btn.pack(side="left")
        self.macro_8_indicator = tk.Canvas(self.macro_8_frame, width=20, height=20)
        self.macro_8_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
        self.macro_8_indicator.pack(side="right")
        
        # Q 매크로 버튼 (일회성 실행)
        self.macro_q_frame = tk.Frame(self.root)
        self.macro_q_frame.pack(pady=5)
        self.macro_q_btn = tk.Button(
            self.macro_q_frame, 
            text="Q 매크로 실행", 
            command=self.execute_macro_q, 
            bg="#AED6F1", 
            state='disabled'  # 기본 매크로가 꺼졌을 때 비활성화
        )
        self.macro_q_btn.pack(side="left")
        self.macro_q_indicator = tk.Canvas(self.macro_q_frame, width=20, height=20)
        self.macro_q_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
        self.macro_q_indicator.pack(side="right")
        
        # 힐 매크로 버튼 (일회성 실행)
        self.macro_heal_frame = tk.Frame(self.root)
        self.macro_heal_frame.pack(pady=5)
        self.macro_heal_btn = tk.Button(
            self.macro_heal_frame, 
            text="힐 매크로 실행", 
            command=self.execute_macro_heal, 
            bg="#58D68D",  # 원하는 색상으로 설정
            state='disabled'  # 기본 매크로가 꺼졌을 때 비활성화
        )
        self.macro_heal_btn.pack(side="left")
        self.macro_heal_indicator = tk.Canvas(self.macro_heal_frame, width=20, height=20)
        self.macro_heal_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
        self.macro_heal_indicator.pack(side="right")
        
        # Bomu 매크로 버튼 (토글 실행)
        self.macro_bomu_frame = tk.Frame(self.root)
        self.macro_bomu_frame.pack(pady=5)
        self.macro_bomu_btn = tk.Button(
            self.macro_bomu_frame, 
            text="Bomu 매크로 ON", 
            command=self.toggle_macro_bomu, 
            bg="#F39C12",  # 원하는 색상으로 설정
            state='disabled'  # 기본 매크로가 꺼졌을 때 비활성화
        )
        self.macro_bomu_btn.pack(side="left")
        self.macro_bomu_indicator = tk.Canvas(self.macro_bomu_frame, width=20, height=20)
        self.macro_bomu_indicator.create_oval(5, 5, 15, 15, fill="red", tags="circle")
        self.macro_bomu_indicator.pack(side="right")
        
        # 상태 표시 레이블
        self.status_label = tk.Label(self.root, text="매크로 상태: OFF")
        self.status_label.pack(pady=10)
    
    def set_macros(self, macros):
        self.macros = macros
    
    def toggle_base_macro(self):
        if 'base' in self.macros:
            self.macros['base'].toggle()
            if self.macros['base'].running:
                self.base_macro_btn.config(bg="#4D4D4D", text="기본 매크로 OFF")
                # 다른 매크로 버튼 활성화
                self.macro_7_btn.config(state='normal')
                self.macro_8_btn.config(state='normal')
                self.macro_q_btn.config(state='normal')
                self.macro_heal_btn.config(state='normal')
                self.macro_bomu_btn.config(state='normal')  # Bomu 매크로 버튼 활성화
            else:
                self.base_macro_btn.config(bg="#A9DFBF", text="기본 매크로 ON")
                # 다른 매크로 버튼 비활성화 및 상태 초기화
                # 모든 매크로를 끄기
                for macro_name, macro in self.macros.items():
                    if macro_name != 'base' and hasattr(macro, 'toggle') and macro.running:
                        macro.toggle()
                self.macro_7_btn.config(state='disabled')
                self.macro_7_indicator.itemconfig("circle", fill="red")
                self.macro_8_btn.config(state='disabled')
                self.macro_8_indicator.itemconfig("circle", fill="red")
                self.macro_q_btn.config(state='disabled')
                self.macro_q_indicator.itemconfig("circle", fill="red")
                self.macro_heal_btn.config(state='disabled')
                self.macro_heal_indicator.itemconfig("circle", fill="red")
                self.macro_bomu_btn.config(state='disabled')
                self.macro_bomu_indicator.itemconfig("circle", fill="red")
    
    def toggle_macro_7(self):
        if 'macro_7' in self.macros:
            self.macros['macro_7'].toggle()
            if self.macros['macro_7'].running:
                self.macro_7_btn.config(bg="#CD6155", text="7키 매크로 OFF")
            else:
                self.macro_7_btn.config(bg="#F1948A", text="7키 매크로 ON")
    
    def toggle_macro_8(self):
        if 'macro_8' in self.macros:
            self.macros['macro_8'].toggle()
            if self.macros['macro_8'].running:
                self.macro_8_btn.config(bg="#5DADE2", text="8키 매크로 OFF")
            else:
                self.macro_8_btn.config(bg="#85C1E9", text="8키 매크로 ON")
    
    def execute_macro_q(self):
        if 'macro_q' in self.macros:
            self.macros['macro_q'].execute()
            self.macro_q_indicator.itemconfig("circle", fill="green")
    
    def execute_macro_heal(self):
        if 'macro_heal' in self.macros:
            self.macros['macro_heal'].execute()
            self.macro_heal_indicator.itemconfig("circle", fill="green")
    
    def toggle_macro_bomu(self):
        if 'macro_bomu' in self.macros:
            self.macros['macro_bomu'].toggle()
            if self.macros['macro_bomu'].running:
                self.macro_bomu_btn.config(bg="#D35400", text="Bomu 매크로 OFF")
            else:
                self.macro_bomu_btn.config(bg="#F39C12", text="Bomu 매크로 ON")
