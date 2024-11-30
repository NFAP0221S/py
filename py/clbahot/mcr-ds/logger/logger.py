# logger/logger.py

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class Logger:
    def __init__(self, parent):
        self.log_text = ScrolledText(parent, height=15, state='disabled', wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, padx=10, pady=10)
        self.log_index = 1

    def log_message(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{self.log_index}번째 Log: {message}\n")
        self.log_text.config(state='disabled')
        self.log_text.yview(tk.END)
        self.log_index += 1
