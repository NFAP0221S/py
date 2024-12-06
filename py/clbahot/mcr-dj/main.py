# main.py

import tkinter as tk

import keyboard
import pyautogui
from gui.main_gui import MainGUI
from macros.base_macro import BaseMacro
from macros.macro_7 import Macro7
from macros.macro_8 import Macro8
from macros.macro_9 import Macro9
from macros.macro_q import MacroQ
from macros.macro_ddp import MacroDDP
from macros.macro_bomu import MacroBomu
from listeners.key_listener import KeyListener
from logger.logger import Logger
from utils.indicators import update_indicator

def main():
    # Tkinter 루트 초기화
    root = tk.Tk()
    root.title("매크로 제어")
    root.geometry("500x700")  # 창 크기를 조정

    # 로거 초기화
    logger = Logger(root)

    # GUI 초기화
    gui = MainGUI(root, logger)

    # 매크로 초기화
    macros = {
        # 'base': BaseMacro(
        #     log_function=logger.log_message,
        #     update_indicator_func=lambda state: update_indicator(gui.base_macro_indicator, state),
        #     turn_off_all_macros_func=lambda: turn_off_all_macros(macros, gui)
        # ),
        # 'macro_7': Macro7(
        #     log_function=logger.log_message,
        #     update_indicator_func=lambda state: update_indicator(gui.macro_7_indicator, state)
        # ),
        # 'macro_8': Macro8(
        #     log_function=logger.log_message,
        #     update_indicator_func=lambda state: update_indicator(gui.macro_8_indicator, state)
        # ),
        # 'macro_9': Macro9(
        #     log_function=logger.log_message,
        #     update_indicator_func=lambda state: update_indicator(gui.macro_9_indicator, state)
        # ),
        # 'macro_q': MacroQ(
        #     log_function=logger.log_message
        # ),
        
        'macro_ddp': MacroDDP(
            log_function=logger.log_message
        ),
        # 'macro_bomu': MacroBomu(
        #     log_function=logger.log_message,
        #     update_indicator_func=lambda state: update_indicator(gui.macro_bomu_indicator, state)
        # )
    }

    # GUI에 매크로 전달
    gui.set_macros(macros)

    # 키 리스너 초기화 (Bomu 매크로는 버튼으로만 제어)
    def on_press(key):
        try:
            # if key.char == '[':
            #     macros['base'].toggle()
            # elif key.char == ']':
            #     macros['macro_7'].toggle()
            # elif key.char == '\\':
            #     macros['macro_8'].toggle()
            # elif key.char == '=':
            #     macros['macro_9'].toggle()
            # elif key.char == 'q':
            #     macros['macro_q'].execute()
            if key.char == '`':
                pyautogui.press('u')
                pyautogui.press('u')
                pyautogui.press('u')
                pyautogui.press('u')
                pyautogui.press('6')
            elif key.char == '2':
                pyautogui.press('a')
                # pyautogui.press('5')
            # elif key.char == 'z':
            #     pyautogui.press(',')
            # elif key == keyboard.Key.insert:
            #     pyautogui.press('7')
            #     pyautogui.press('home')
            #     pyautogui.press('enter')
            # elif key == keyboard.Key.insert:
            #     pyautogui.press('7')
            #     pyautogui.press('home')
            #     pyautogui.press('enter')
            # Bomu 매크로는 버튼으로만 제어
            # elif key.char == 'b':  # 필요 시 추가
            #     macros['macro_bomu'].toggle()
        except AttributeError:
            pass

    def on_release(key):
        pass

    listener = KeyListener(on_press, on_release)
    listener.start()

    # GUI 루프 시작
    root.mainloop()

def turn_off_all_macros(macros, gui):
    # 기본 매크로를 제외한 모든 매크로를 끄기
    for macro_name, macro in macros.items():
        if macro_name != 'base' and hasattr(macro, 'toggle') and macro.running:
            macro.toggle()
    
    # GUI에서 모든 매크로 버튼 상태 업데이트
    gui.macro_7_btn.config(state='disabled')
    gui.macro_7_indicator.itemconfig("circle", fill="red")
    gui.macro_8_btn.config(state='disabled')
    gui.macro_8_indicator.itemconfig("circle", fill="red")
    gui.macro_9_btn.config(state='disabled')
    gui.macro_9_indicator.itemconfig("circle", fill="red")
    gui.macro_q_btn.config(state='disabled')
    gui.macro_q_indicator.itemconfig("circle", fill="red")
    gui.macro_heal_btn.config(state='disabled')
    gui.macro_heal_indicator.itemconfig("circle", fill="red")
    gui.macro_bomu_btn.config(state='disabled')
    gui.macro_bomu_indicator.itemconfig("circle", fill="red")

if __name__ == "__main__":
    main()
