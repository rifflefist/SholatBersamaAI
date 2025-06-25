import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def start(event):
    messagebox.showinfo("Info", "Camera terbuka")

def settings():
    messagebox.showinfo("Info", "Settings terbuka")

def quit_app():
    window.destroy()
    
def on_enter(e):
    e.widget['background'] = '#007acc'  # Warna saat hover
    e.widget['foreground'] = 'white'
    e.widget.config(cursor="hand2")

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'  # Warna default
    e.widget['foreground'] = 'black'
    e.widget.config(cursor="")
    
def on_enter_play(e):
    label_play.config(image=play_img_hover)
    e.widget.config(cursor="hand2")

def on_leave_play(e):
    label_play.config(image=play_img)
    e.widget.config(cursor="")

window = tk.Tk()
window.title("Sholat Bersama AI")
# window.state("zoomed")
window.configure(bg="lightblue")
window.minsize(800, 600)

img = Image.open("assets/images/play.png").resize((300, 300), Image.LANCZOS)
play_img = ImageTk.PhotoImage(img)

img_hover = Image.open("assets/images/play_hover.png").resize((300, 300), Image.LANCZOS)
play_img_hover = ImageTk.PhotoImage(img_hover)

label_play = tk.Label(window, image=play_img, bg="#add8e6", borderwidth=0)
label_play.place(relx=0.5, rely=0.3, anchor="center")
label_play.bind("<Button-1>", start)
label_play.bind("<Enter>", on_enter_play)
label_play.bind("<Leave>", on_leave_play)

# Tombol Settings (kiri bawah)
btn_settings = tk.Button(window, text="Settings", font=("Arial", 16), command=settings)
btn_settings.place(relx=0.3, rely=0.75, anchor="center", width=0.25*1080, relheight=0.1)
btn_settings.bind("<Enter>", on_enter)
btn_settings.bind("<Leave>", on_leave)

# Tombol Quit (kanan bawah)
btn_quit = tk.Button(window, text="Quit", font=("Arial", 16), command=quit_app)
btn_quit.place(relx=0.7, rely=0.75, anchor="center", width=0.25*1080, relheight=0.1)
btn_quit.bind("<Enter>", on_enter)
btn_quit.bind("<Leave>", on_leave)

window.mainloop()
