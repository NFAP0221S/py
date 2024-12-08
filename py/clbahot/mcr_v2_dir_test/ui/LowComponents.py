import tkinter as tk

def 생성_로우(scroll_frame, index, set_area_callback, set_mp_area_callback, toggle_mp_monitoring_callback):
    # 개별 Low를 구성하는 함수
    low_frame = tk.Frame(scroll_frame, pady=5, relief="ridge", borderwidth=2)
    low_frame.pack(fill="x", padx=5, pady=5)

    # 로우 구성 요소들
    tk.Label(low_frame, text=f"Low {index+1} 제목:").pack(side="left", padx=5)
    제목_입력 = tk.Entry(low_frame, width=10)
    제목_입력.pack(side="left", padx=5)

    tk.Label(low_frame, text="입력 값:").pack(side="left", padx=5)
    값_입력 = tk.Entry(low_frame, width=10)
    값_입력.pack(side="left", padx=5)

    tk.Label(low_frame, text="설명:").pack(side="left", padx=5)
    설명_입력 = tk.Entry(low_frame, width=15)
    설명_입력.pack(side="left", padx=5)

    if index == 2:
        # 3번째 Low (MP 바 영역 설정 전용)
        mp_버튼 = tk.Button(low_frame, text="MP 영역 설정", command=set_mp_area_callback)
        mp_버튼.pack(side="left", padx=5)

        토글_버튼 = tk.Button(low_frame, text="OFF", bg="red", command=toggle_mp_monitoring_callback)
        토글_버튼.pack(side="left", padx=5)

        low_item = {
            "title": 제목_입력,
            "value": 값_입력,
            "description": 설명_입력,
            "set_mp_button": mp_버튼,
            "toggle_button": 토글_버튼,
            "mp_area": None,
            "monitoring": False,
            "log_text": None,
        }
    else:
        영역_버튼 = tk.Button(low_frame, text="영역 설정", command=lambda idx=index: set_area_callback(idx))
        영역_버튼.pack(side="left", padx=5)

        low_item = {
            "title": 제목_입력,
            "value": 값_입력,
            "description": 설명_입력,
            "area_button": 영역_버튼,
            "log_text": None,
        }

    # 로그 텍스트 영역
    로그_텍스트 = tk.Text(low_frame, height=5, width=60, state="disabled")
    로그_텍스트.pack(pady=5)
    low_item["log_text"] = 로그_텍스트

    return low_item
