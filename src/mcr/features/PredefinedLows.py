from mcr.ui.LowComponents import 생성_로우

def 생성_선정된_로우들(scroll_frame, low_items, set_area_callback, set_mp_area_callback, toggle_mp_monitoring_callback):
    # 사전에 정의된 3개의 Low 생성
    for i in range(3):
        low_item = 생성_로우(scroll_frame, i, set_area_callback, set_mp_area_callback, toggle_mp_monitoring_callback)
        low_items.append(low_item)
