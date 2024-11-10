from .base_macro import macro_running, macro_paused
from .m_mabi import macro_8_running
from .m_joongdok import macro_9_running

def toggle_pause_all():
    global macro_paused
    macro_paused = not macro_paused
    if macro_paused:
        print("모든 매크로 일시 중지")
    else:
        print("모든 매크로 재개")

def stop_all_macros():
    global macro_running, macro_8_running, macro_9_running, macro_paused
    macro_running = False
    macro_8_running = False
    macro_9_running = False
    macro_paused = False
    print("모든 상태가 False 되었습니다.")
