# macros/base_macro.py

class BaseMacro:
    def __init__(self, log_function, update_indicator_func, turn_off_all_macros_func):
        self.running = False
        self.log = log_function
        self.update_indicator = update_indicator_func
        self.turn_off_all_macros = turn_off_all_macros_func

    def toggle(self):
        self.running = not self.running
        if self.running:
            self.log("기본 매크로 ON")
            self.update_indicator(True)
        else:
            self.log("기본 매크로 OFF")
            self.update_indicator(False)
            self.turn_off_all_macros()  # 기본 매크로가 꺼질 때 모든 매크로 끄기
