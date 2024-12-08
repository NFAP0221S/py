import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import pyautogui
import time
import threading


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Program")
        self.root.geometry("800x800")  # Adjusted height for logs

        # Create Main Frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Scrollable Canvas Setup
        self.canvas = tk.Canvas(main_frame, width=500, height=750)
        self.scroll_frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Add predefined lows
        self.low_items = []
        self.create_predefined_lows()

    def create_predefined_lows(self):
        for i in range(3):  # Create 3 predefined lows
            low_frame = tk.Frame(self.scroll_frame, pady=5, relief="ridge", borderwidth=2)
            low_frame.pack(fill="x", padx=5, pady=5)

            # Components of "low"
            tk.Label(low_frame, text=f"Low {i+1} Title:").pack(side="left", padx=5)
            title_entry = tk.Entry(low_frame, width=10)
            title_entry.pack(side="left", padx=5)

            tk.Label(low_frame, text="Input Value:").pack(side="left", padx=5)
            value_entry = tk.Entry(low_frame, width=10)
            value_entry.pack(side="left", padx=5)

            tk.Label(low_frame, text="Description:").pack(side="left", padx=5)
            description_entry = tk.Entry(low_frame, width=15)
            description_entry.pack(side="left", padx=5)

            if i == 2:  # Special functionality for the 3rd low
                set_mp_button = tk.Button(low_frame, text="Set MP Bar", command=self.set_mp_area)
                set_mp_button.pack(side="left", padx=5)

                toggle_button = tk.Button(low_frame, text="OFF", bg="red", command=self.toggle_mp_monitoring)
                toggle_button.pack(side="left", padx=5)

                self.low_items.append({
                    "title": title_entry,
                    "value": value_entry,
                    "description": description_entry,
                    "set_mp_button": set_mp_button,
                    "toggle_button": toggle_button,
                    "mp_area": None,  # Placeholder for MP bar area
                    "monitoring": False,  # Tracking MP monitoring state
                    "log_text": None,  # Log text widget
                })
            else:
                area_button = tk.Button(low_frame, text="Set Area", command=lambda idx=i: self.set_area(idx))
                area_button.pack(side="left", padx=5)

                self.low_items.append({
                    "title": title_entry,
                    "value": value_entry,
                    "description": description_entry,
                    "area_button": area_button,
                    "log_text": None,  # Log text widget
                })

            # Add a log text area below each low
            log_text = tk.Text(low_frame, height=5, width=60, state="disabled")
            log_text.pack(pady=5)
            self.low_items[i]["log_text"] = log_text

    def set_area(self, idx):
        self.select_area(idx, f"Area set for Low {idx + 1}")

    def set_mp_area(self):
        self.select_area(2, "MP Bar Area Set")

    def select_area(self, idx, message):
        screen_width, screen_height = pyautogui.size()
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        overlay = frame.copy()
        alpha = 0.3
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        x1, y1 = -1, -1
        drawing = False

        def draw_rectangle(event, x, y, flags, param):
            nonlocal x1, y1, drawing, frame
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                x1, y1 = x, y
            elif event == cv2.EVENT_MOUSEMOVE:
                if drawing:
                    temp_frame = frame.copy()
                    cv2.rectangle(temp_frame, (x1, y1), (x, y), (0, 255, 0), 2)
                    cv2.imshow("Set Area", temp_frame)
            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False
                x2, y2 = x, y
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.imshow("Set Area", frame)
                self.low_items[idx]["mp_area"] = (x1, y1, x2, y2)
                cv2.destroyAllWindows()
                messagebox.showinfo("Area Selected", message)

        cv2.namedWindow("Set Area", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Set Area", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Set Area", frame)
        cv2.setMouseCallback("Set Area", draw_rectangle)
        cv2.waitKey(0)

    def toggle_mp_monitoring(self):
        mp_area = self.low_items[2].get("mp_area")
        input_value_entry = self.low_items[2]["value"]  # Input Value entry widget
        toggle_button = self.low_items[2]["toggle_button"]
        log_text = self.low_items[2]["log_text"]

        if not mp_area:
            messagebox.showerror("Error", "Please set the MP bar area first.")
            return

        if not self.low_items[2]["monitoring"]:
            # Start monitoring
            def monitor_mp():
                while self.low_items[2]["monitoring"]:
                    x1, y1, x2, y2 = mp_area
                    screenshot = pyautogui.screenshot()
                    frame = np.array(screenshot)
                    mp_bar = frame[y1:y2, x1:x2]
                    gray = cv2.cvtColor(mp_bar, cv2.COLOR_BGR2GRAY)
                    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                    white_pixels = cv2.countNonZero(thresh)
                    total_pixels = mp_bar.shape[0] * mp_bar.shape[1]
                    mp_percentage = (white_pixels / total_pixels) * 100

                    try:
                        input_value = float(input_value_entry.get())
                        adjusted_mp_percentage = (mp_percentage / input_value) * 100
                        log_message = f"Adjusted MP: {adjusted_mp_percentage:.2f}%"
                    except ValueError:
                        log_message = f"Current MP: {mp_percentage:.2f}%"

                    print(log_message)

                    log_text.config(state="normal")
                    log_text.insert("end", log_message + "\n")
                    log_text.see("end")
                    log_text.config(state="disabled")

                    time.sleep(1)

            self.low_items[2]["monitoring"] = True
            toggle_button.config(text="ON", bg="green")
            monitoring_thread = threading.Thread(target=monitor_mp, daemon=True)
            monitoring_thread.start()
        else:
            # Stop monitoring
            self.low_items[2]["monitoring"] = False
            toggle_button.config(text="OFF", bg="red")
            messagebox.showinfo("Monitoring", "MP monitoring stopped.")

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
