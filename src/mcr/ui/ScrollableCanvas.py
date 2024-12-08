import tkinter as tk

def 생성_스크롤러블_캔버스(부모, 폭=500, 높이=750):
    # 스크롤 가능 캔버스 구성
    canvas = tk.Canvas(부모, width=폭, height=높이)
    scroll_frame = tk.Frame(canvas)
    scrollbar = tk.Scrollbar(부모, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    scroll_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    return canvas, scroll_frame, scrollbar
