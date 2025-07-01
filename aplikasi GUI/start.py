import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
from assets.helper.get_resource import resource_path
from assets.helper.get_camera import get_camera
from assets.helper.save_settings import load_settings
from assets.helper.get_time import get_salat_time

class Start(tk.Frame):
    my_bg = "lighblue"

    def __init__(self, parent, show_next):
        super().__init__(parent)
        self.show_next = show_next  # Disimpan agar bisa dipanggil nanti
        self.configure(bg=self.my_bg)
        self.build_ui()

    def build_ui(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        image_width = 75
        image_height = 50
        
        settings = load_settings()
        
        img = Image.open(resource_path("assets/images/arrow.png")).resize((image_width, image_height), Image.LANCZOS)
        self.back_img = ImageTk.PhotoImage(img)
        
        img = Image.open(resource_path("assets/images/arrow_hover.png")).resize((image_width, image_height), Image.LANCZOS)
        self.back_hover_img = ImageTk.PhotoImage(img)
        
        self.label_back = tk.Label(self, image=self.back_img, bg=self.my_bg, borderwidth=0)
        self.label_back.place(relx=0.01, rely=0.01, anchor="nw")
        self.label_back.bind("<Button-1>", self.back)
        self.label_back.bind("<Enter>", self.on_enter)
        self.label_back.bind("<Leave>", self.on_leave)
        
        jam_atas_frame = tk.Frame(self, bg=self.my_bg)
        jam_atas_frame.place(relx=1, rely=0.0, anchor="ne")

        jam_frame = tk.Frame(jam_atas_frame, bg=self.my_bg)
        jam_frame.place(relx=1.0, rely=0.0, anchor="ne")
        
        self.label_hour = tk.Label(jam_frame, text="--", font=("Arial", 40, "bold"), bg=self.my_bg)
        self.label_colon = tk.Label(jam_frame, text=":", font=("Arial", 40, "bold"), bg=self.my_bg)
        self.label_minute = tk.Label(jam_frame, text="--", font=("Arial", 40, "bold"), bg=self.my_bg)
        
        self.start_time = datetime.strptime(settings["time"], "%H:%M")
        self.run_start = datetime.now()
        
        self.label_hour.pack(side="left")
        self.label_colon.pack(side="left")
        self.label_minute.pack(side="left")
        
        self.visible = True
        self.update_time()
        self.blink_colon()
        
        font_size = max(10, int(min(screen_width, screen_height) * 0.03))
        judul = tk.Label(jam_atas_frame, text=get_salat_time(settings["time"]), bg=self.my_bg, font=("Arial", font_size, "bold"))
        judul.pack(side="left")
        
        frame_mid = tk.Frame(self, bg="black")
        frame_mid.place(relx=0.5, rely=0.48, relwidth=0.65, relheight=0.8, anchor="center")
        
        frame_set = tk.Frame(self, bg=self.my_bg)
        frame_set.place(relx=0.2, rely=0.92, relheight=0.2, relwidth=0.6, anchor="nw")

        frame_set.rowconfigure(0, weight=0)
        frame_set.columnconfigure(0, weight=1)
        frame_set.columnconfigure(1, weight=2)
        frame_set.columnconfigure(2, weight=2)
        frame_set.columnconfigure(3, weight=1) 
        
        spacer = tk.Label(frame_set, bg=self.my_bg)
        spacer.grid(row=0, column=0, sticky="nsew")

        kamera_list = get_camera()
        
        kamera_default = self.camera
        self.pilihan = tk.StringVar(value=kamera_list[kamera_default])

        self.dropdown_kamera = tk.Label(frame_set, text="▲  " + self.pilihan.get(), font=("Arial", 14, "bold"), anchor="w", borderwidth=2, relief="solid")
        self.dropdown_kamera.grid(row=0, column=1, sticky="nsew")
        self.dropdown_kamera.bind("<Button-1>", lambda e: self.toggle_dropdown())
        self.dropdown_kamera.bind("<Enter>", self.hover)
        
        self.count_kamera = len(kamera_list)
        self.listbox = tk.Listbox(self, font=("Arial", 12, "bold"), height=self.count_kamera)
        for item in kamera_list:
            self.listbox.insert(tk.END, item)

        self.listbox.bind("<<ListboxSelect>>", self.pilih)
        self.listbox.bind("<Enter>", self.hover)

        orientation = ["Landscape", "Portrait"]

        orientation_set = settings["orientation"]

        self.pilihan_orientation = tk.StringVar(value=orientation[orientation_set])

        self.dropdown_orientation = tk.Label(frame_set, text="▲  " + self.pilihan_orientation.get(), font=("Arial", 14, "bold"), anchor="w", borderwidth=2, relief="solid")
        self.dropdown_orientation.grid(row=0, column=2, sticky="nsew")
        self.dropdown_orientation.bind("<Button-1>", lambda e: self.toggle_dropdown_orientation())
        self.dropdown_orientation.bind("<Enter>", self.hover)
        
        self.listbox_orientation = tk.Listbox(self, font=("Arial", 12, "bold"), height=len(orientation))
        for item1 in orientation:
            self.listbox_orientation.insert(tk.END, item1)

        self.listbox_orientation.bind("<<ListboxSelect>>", self.pilih_orientation)
        self.listbox_orientation.bind("<Enter>", self.hover)

        spacer1 = tk.Label(frame_set, bg=self.my_bg)
        spacer1.grid(row=0, column=3, sticky="nsew")
    
    settings = load_settings()
    # Kalau udah ada settings.ini diubah
    camera = settings["camera"]
    orientation = settings["orientation"]
    time = settings["time"]

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
    
    def toggle_dropdown(self):
        if self.listbox.winfo_ismapped():
            self.listbox.place_forget()
            self.unbind_all("<Button-1>")
        else:
            self.listbox.place(relx=0.3, rely=0.92, relwidth=0.18, anchor="sw")
            self.listbox.lift()
            self.after(100, lambda: self.bind_all("<Button-1>", self.on_global_click))
    
    def on_global_click(self, event):
        widget = event.widget
        if widget != self.listbox and widget != self.dropdown_kamera:
            self.listbox.place_forget()
            self.unbind_all("<Button-1>")
    
    def pilih(self, e):
        if self.listbox.curselection():
            pilihan = self.listbox.get(self.listbox.curselection())
            self.pilihan.set(pilihan)
            self.dropdown_kamera.config(text="▲  " + pilihan)
            self.listbox.place_forget()
    
    def toggle_dropdown_orientation(self):
        if self.listbox_orientation.winfo_ismapped():
            self.listbox_orientation.place_forget()
            self.unbind_all("<Button-1>")
        else:
            self.listbox_orientation.place(relx=0.57, rely=0.92, relwidth=0.12, anchor="sw")
            self.listbox_orientation.lift()
            self.after(100, lambda: self.bind_all("<Button-1>", self.on_global_click_orientation))
    
    def on_global_click_orientation(self, event):
        widget = event.widget
        if widget != self.listbox_orientation and widget != self.dropdown_orientation:
            self.listbox_orientation.place_forget()
            self.unbind_all("<Button-1>")
    
    def pilih_orientation(self, e):
        if self.listbox_orientation.curselection():
            pilihan = self.listbox_orientation.get(self.listbox_orientation.curselection())
            self.pilihan_orientation.set(pilihan)
            self.dropdown_orientation.config(text="▲  " + pilihan)
            self.listbox_orientation.place_forget()