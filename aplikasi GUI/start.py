import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
from assets.helper.get_resource import resource_path
from assets.helper.save_settings import load_settings
from assets.helper.get_time import get_salat_time

class Start(tk.Frame):
    def __init__(self, parent, show_next):
        super().__init__(parent)
        self.show_next = show_next  # Disimpan agar bisa dipanggil nanti
        self.configure(bg="#add8e6")
        self.build_ui()

    def build_ui(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        image_width = 100
        image_height = 75
        
        settings = load_settings()
        
        img = Image.open(resource_path("assets/images/arrow.png")).resize((image_width, image_height), Image.LANCZOS)
        self.back_img = ImageTk.PhotoImage(img)
        
        img = Image.open(resource_path("assets/images/arrow_hover.png")).resize((image_width, image_height), Image.LANCZOS)
        self.back_hover_img = ImageTk.PhotoImage(img)
        
        self.label_back = tk.Label(self, image=self.back_img, bg="#add8e6", borderwidth=0)
        self.label_back.place(relx=0.01, rely=0.01, anchor="nw")
        self.label_back.bind("<Button-1>", self.back)
        self.label_back.bind("<Enter>", self.on_enter)
        self.label_back.bind("<Leave>", self.on_leave)
        
        jam_frame = tk.Frame(self, bg="lightblue")
        jam_frame.place(relx=1.0, rely=0.0, anchor="ne")
        
        self.label_hour = tk.Label(jam_frame, text="--", font=("Arial", 40, "bold"), bg="lightblue")
        self.label_colon = tk.Label(jam_frame, text=":", font=("Arial", 40, "bold"), bg="lightblue")
        self.label_minute = tk.Label(jam_frame, text="--", font=("Arial", 40, "bold"), bg="lightblue")
        
        self.start_time = datetime.strptime(settings["time"], "%H:%M")
        self.run_start = datetime.now()
        
        self.label_hour.pack(side="left")
        self.label_colon.pack(side="left")
        self.label_minute.pack(side="left")
        
        self.visible = True
        self.update_time()
        self.blink_colon()
        
        font_size = max(10, int(min(screen_width, screen_height) * 0.03))
        judul = tk.Label(self, text=get_salat_time(settings["time"]), bg="#add8e6", font=("Arial", font_size, "bold"))
        judul.place(relx=0.99, rely=0.12, anchor="ne")
    
    def back(self, e):
        self.show_next("homepage")
    
    def on_enter(self, e):
        self.label_back.config(image=self.back_hover_img)
        e.widget.config(cursor="hand2")
        
    def hover(self, e):
        e.widget.config(cursor="hand2")

    def on_leave(self, e):
        self.label_back.config(image=self.back_img)
        e.widget.config(cursor="")
    
    def update_time(self):
        # Hitung waktu berjalan sejak app start
        elapsed = datetime.now() - self.run_start
        current_time = self.start_time + elapsed

        hour = current_time.strftime("%H")
        minute = current_time.strftime("%M")

        self.label_hour.config(text=hour)
        self.label_minute.config(text=minute)

        self.after(1000, self.update_time)

    def blink_colon(self):
        self.visible = not self.visible
        self.label_colon.config(fg="black" if self.visible else self["bg"])
        self.after(500, self.blink_colon)