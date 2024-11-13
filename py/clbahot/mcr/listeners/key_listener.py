# listeners/key_listener.py

from pynput import keyboard

class KeyListener:
    def __init__(self, on_press_callback, on_release_callback):
        self.listener = keyboard.Listener(on_press=on_press_callback, on_release=on_release_callback)
    
    def start(self):
        self.listener.start()
    
    def stop(self):
        self.listener.stop()
