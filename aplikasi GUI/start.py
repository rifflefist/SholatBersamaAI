import tkinter as tk

class Start(tk.Frame):
    def __init__(self, parent, show_next):
        super().__init__(parent)
        self.show_next = show_next  # Disimpan agar bisa dipanggil nanti
        self.configure(bg="#add8e6")
        self.build_ui()

    def build_ui(self):
        tk.Button(self, text="Ke Halaman Homepage", command=self.back).pack()
    
    def back(self):
        self.show_next("homepage")