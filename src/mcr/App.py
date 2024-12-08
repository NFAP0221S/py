import tkinter as tk
from tkinter import messagebox
import threading

# 기능 모듈 임포트
from mcr.ui.MainFrame import MainFrame
from mcr.features.PredefinedLows import 생성_선정된_로우들
from mcr.features.AreaSelection import 영역_선택
from mcr.features.MPMonitoring import 시작_MP모니터링

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("커스텀 프로그램")
        self.root.geometry("800x800")  # 창 크기 설정

        # 메인 프레임 및 스크롤 캔버스 생성
        self.main_frame, self.canvas, self.scroll_frame, self.scrollbar = MainFrame(self.root)

        # low 아이템 리스트 (로우들의 상태 및 위젯 관리)
        self.low_items = []

        # 사전에 정의된 로우들 생성
        생성_선정된_로우들(
            scroll_frame=self.scroll_frame,
            low_items=self.low_items,
            set_area_callback=self.set_area,
            set_mp_area_callback=self.set_mp_area,
            toggle_mp_monitoring_callback=self.toggle_mp_monitoring
        )

    def set_area(self, idx):
        # 특정 Low에 대한 영역 설정
        메시지 = f"Low {idx + 1}에 대한 영역이 설정되었습니다."
        영역_선택(idx, 메시지, self.low_items)

    def set_mp_area(self):
        # MP 바 영역 설정 (3번째 Low)
        메시지 = "MP 바 영역이 설정되었습니다."
        영역_선택(2, 메시지, self.low_items)

    def toggle_mp_monitoring(self):
        # MP 모니터링 토글
        mp_area = self.low_items[2].get("mp_area")
        입력값_위젯 = self.low_items[2]["value"]
        토글_버튼 = self.low_items[2]["toggle_button"]

        if not mp_area:
            messagebox.showerror("에러", "먼저 MP 바 영역을 설정하세요.")
            return

        if not self.low_items[2]["monitoring"]:
            # 모니터링 시작
            self.low_items[2]["monitoring"] = True
            토글_버튼.config(text="ON", bg="green")
            모니터링_스레드 = threading.Thread(
                target=시작_MP모니터링, 
                args=(self.low_items,), 
                daemon=True
            )
            모니터링_스레드.start()
        else:
            # 모니터링 중지
            self.low_items[2]["monitoring"] = False
            토글_버튼.config(text="OFF", bg="red")
            messagebox.showinfo("모니터링", "MP 모니터링이 중지되었습니다.")
