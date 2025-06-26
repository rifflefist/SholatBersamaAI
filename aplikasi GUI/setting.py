import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Setting(tk.Frame):
    def __init__(self, parent, show_next):
        super().__init__(parent)
        self.show_next = show_next  # Disimpan agar bisa dipanggil nanti
        self.configure(bg="#add8e6")
        self.build_ui()

    def build_ui(self):
        img = Image.open("assets/images/arrow.png").resize((300, 300), Image.LANCZOS)
        self.play_img = ImageTk.PhotoImage(img)
        tk.Button(self, text="Balik ke homepage", command=self.back).pack()
    
    def back(self):
        self.show_next("homepage")