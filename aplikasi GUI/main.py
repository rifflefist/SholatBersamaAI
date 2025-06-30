import tkinter as tk
from homepage import Homepage
from setting import Setting
from start import Start
from assets.style.style import Style

window_width = 800
window_height = 600
window = tk.Tk()
window.title("Sholat Bersama AI")

# window.state("zoomed")
window.configure(bg="lightblue")
window.minsize(800, 600)
Style.center_window(window, window_width, window_height)

def show_next(target_frame):
    
    global frame_setting
    
    frame_setting.pack_forget()
    frame_homepage.pack_forget()
    frame_start.pack_forget()

    if target_frame == "homepage":
        frame_homepage.pack(fill="both", expand=True)
    elif target_frame == "setting":
        frame_setting.destroy()
        frame_setting = Setting(window, show_next)
        frame_setting.pack(fill="both", expand=True)
    elif target_frame == "start":
        frame_start.pack(fill="both", expand=True)

# ⬇️ Kirim fungsi navigasi saat membuat Page
frame_homepage = Homepage(window,show_next)
frame_setting = Setting(window, show_next)
frame_start = Start(window, show_next)

frame_homepage.pack(fill="both", expand=True)

window.mainloop()