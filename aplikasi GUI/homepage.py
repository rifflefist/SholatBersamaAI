import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Homepage(tk.Frame):
    def __init__(self, parent, show_next):
        super().__init__(parent)
        self.show_next = show_next
        self.configure(bg="#add8e6")
        self.build_ui()
    
    def build_ui(self):

        img = Image.open("assets/images/play.png").resize((300, 300), Image.LANCZOS)
        self.play_img = ImageTk.PhotoImage(img)

        img_hover = Image.open("assets/images/play_hover.png").resize((300, 300), Image.LANCZOS)
        self.play_img_hover = ImageTk.PhotoImage(img_hover)

        self.label_play = tk.Label(self, image=self.play_img, bg="#add8e6", borderwidth=0)
        self.label_play.place(relx=0.5, rely=0.3, anchor="center")
        self.label_play.bind("<Button-1>", self.start)
        self.label_play.bind("<Enter>", self.on_enter_play)
        self.label_play.bind("<Leave>", self.on_leave_play)

        # Tombol Settings (kiri bawah)
        btn_settings = tk.Button(self, text="Settings", font=("Arial", 16), command=self.settings)
        btn_settings.place(relx=0.3, rely=0.75, anchor="center", width=0.25*1080, relheight=0.1)
        btn_settings.bind("<Enter>", self.on_enter)
        btn_settings.bind("<Leave>", self.on_leave)

        # Tombol Quit (kanan bawah)
        btn_quit = tk.Button(self, text="Quit", font=("Arial", 16), command=self.quit_app)
        btn_quit.place(relx=0.7, rely=0.75, anchor="center", width=0.25*1080, relheight=0.1)
        btn_quit.bind("<Enter>", self.on_enter)
        btn_quit.bind("<Leave>", self.on_leave)


    def start(self, e):
        self.show_next("start")

    def settings(self):
        self.show_next("setting")

    def quit_app(self):
        hasil =  messagebox.askyesno("Warning", "Do you want to quit?")

        if hasil:
            self.winfo_toplevel().destroy()
        else:
            pass

        
    def on_enter(self, e):
        e.widget['background'] = '#007acc'  # Warna saat hover
        e.widget['foreground'] = 'white'
        e.widget.config(cursor="hand2")

    def on_leave(self, e):
        e.widget['background'] = 'SystemButtonFace'  # Warna default
        e.widget['foreground'] = 'black'
        e.widget.config(cursor="")
        
    def on_enter_play(self, e):
        self.label_play.config(image=self.play_img_hover)
        e.widget.config(cursor="hand2")

    def on_leave_play(self, e):
        self.label_play.config(image=self.play_img)
        e.widget.config(cursor="")
