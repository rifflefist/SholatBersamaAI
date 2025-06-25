# Import Module
from tkinter import *
from tkinter import messagebox
import tkinter as tk

# create root window
window = tk.Tk()

window.geometry("500x500")

# root window title and dimension
window.title("Sholat Bersama AI")

window.state("zoomed")

y_size = window.winfo_screenheight()
x_size = window.winfo_screenwidth()

color_bg = "lightblue"

frame1 = tk.Frame(window, width=x_size, height=y_size, bg=color_bg, relief=tk.SOLID)
frame1.pack(padx=0, pady=0)

def start():
    messagebox.showinfo("informasi", "Camera terbuka")

def settings():
    messagebox.showinfo("informasi", "Settings terbuka")
    # frame1.destroy()

def quit():
    window.destroy()

play_button = PhotoImage(file=r"play.png")

btn_size_play = 300
btn = Button(frame1, text="Button", command=start, width=btn_size_play, height=btn_size_play, image=play_button, bg=color_bg)

btn.place(x=(x_size-btn_size_play)/2, y=(y_size-btn_size_play)*0.2)

btn_size_setting_x = 50
btn_size_setting_y = 10
btn1 = Button(frame1, text="Settings", command=settings, width=btn_size_setting_x, height=btn_size_setting_y, bg=color_bg)
btn1.place(x=(x_size-btn_size_setting_x)*0.25, y=(y_size-btn_size_setting_y)*0.6)

btn1 = Button(frame1, text="Quit", command=quit, width=btn_size_setting_x, height=btn_size_setting_y, bg=color_bg)
btn1.place(x=(x_size-btn_size_setting_x)*0.6, y=(y_size-btn_size_setting_y)*0.6)

# all widgets will be here
# Execute Tkinter
window.mainloop()