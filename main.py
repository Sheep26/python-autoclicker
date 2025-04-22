from pynput import keyboard
from pynput.mouse import Button, Controller
import tkinter as tk
from tkinter import messagebox
from _thread import start_new_thread, interrupt_main
import time
import sys

class AutoClickerUI:
    def __init__(self, root, main):
        self.root = root
        self.root.title("Autoclicker")

        self.cps = 0
        
        self.main = main

        # Create input label and entry
        self.label = tk.Label(root, text="CPS: ")
        self.label.pack(side = "left", pady=10)

        # Validation command for integers only
        vcmd = (root.register(self.validate_int), '%P')
        self.entry = tk.Entry(root, validate='key', validatecommand=vcmd)
        self.entry.pack(side = "left", pady=10, padx=20)

        # Button to save input
        self.button = tk.Button(root, text="Set", command=self.save_input)
        self.button.pack(side="left", pady=10)
        
        self.startStopButton = tk.Button(root, text="Start/Stop (F6)", command=self.startStop)
        self.startStopButton.pack(pady=10, padx=10)
    
    def startStop(self):
        if self.main.running:
            self.main.running = False
        else:
            self.main.running = True
            start_new_thread(self.main.click_thread, ())

    def validate_int(self, new_value):
        """Allow only empty string or valid integer"""
        return new_value == "" or new_value.isdigit()

    def save_input(self):
        text = self.entry.get()
        try:
            self.cps = int(text)
            print(f"Saved value: {self.cps}")
        except:
            messagebox.showwarning("Input Error", "Please enter a number.")

class Main:
    def __init__(self, root, window):
        start_new_thread(self.listener, ())
        self.mouse = Controller()
        self.running = False
        self.app = window(root, self)
        root.mainloop()

    def click_thread(self):
        time.sleep(1)
        while-self.running:
            self.mouse.press(Button.left)
            self.mouse.release(Button.left)
            time.sleep(1/self.app.cps)
        exit(0)
    
    def listener(self):
        # Collect events until released
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        if key == keyboard.Key.f6:
            if self.running:
                self.running = False
            else:
                self.running = True
                start_new_thread(self.click_thread, ())
    
    def on_release(self, key):
        pass

main = Main(tk.Tk(), AutoClickerUI)