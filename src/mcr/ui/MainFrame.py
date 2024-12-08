import tkinter as tk
from mcr.ui.ScrollableCanvas import 생성_스크롤러블_캔버스

def MainFrame(root):
    # 메인 프레임 생성
    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    # 스크롤 가능한 캔버스 생성
    canvas, scroll_frame, scrollbar = 생성_스크롤러블_캔버스(main_frame, 폭=500, 높이=750)

    return main_frame, canvas, scroll_frame, scrollbar
