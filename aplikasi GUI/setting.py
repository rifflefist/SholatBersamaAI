import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from assets.helper.get_resource import resource_path
from assets.helper.get_camera import get_camera

class Setting(tk.Frame):
    def __init__(self, parent, show_next):
        super().__init__(parent)
        self.show_next = show_next
        self.configure(bg="#add8e6")
        self.build_ui()

    def build_ui(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        font_size = max(10, int(min(screen_width, screen_height) * 0.03))
        judul = tk.Label(self, text="Settings", bg="#add8e6", font=("Arial", font_size, "bold"))
        judul.place(relx=0.01, rely=0.01, anchor="nw")
        
        image_width = 75
        image_height = 50
        
        img = Image.open(resource_path("assets/images/arrow.png")).resize((image_width, image_height), Image.LANCZOS)
        self.back_img = ImageTk.PhotoImage(img)
        
        img = Image.open(resource_path("assets/images/arrow_hover.png")).resize((image_width, image_height), Image.LANCZOS)
        self.back_hover_img = ImageTk.PhotoImage(img)
        
        self.label_back = tk.Label(self, image=self.back_img, bg="#add8e6", borderwidth=0)
        self.label_back.place(relx=0.95, rely=0.05, anchor="center")
        self.label_back.bind("<Button-1>", self.back)
        self.label_back.bind("<Enter>", self.on_enter)
        self.label_back.bind("<Leave>", self.on_leave)
        
        title_size = max(10, int(min(screen_width, screen_height) * 0.022))
        judul = tk.Label(self, text="Camera", bg="#add8e6", font=("Arial", title_size, "bold"))
        judul.place(relx=0.14, rely=0.2, anchor="w")
        
        kamera_list = get_camera()
        
        kamera_default = self.camera
        self.pilihan = tk.StringVar(value=kamera_list[kamera_default])
        
        self.dropdown_kamera = tk.Label(self, text="▼  " + self.pilihan.get(), font=("Arial", 14, "bold"), relief="solid", anchor="w")
        self.dropdown_kamera.place(relx=0.17, rely=0.27,  relwidth=0.7, relheight=0.05, anchor="w")
        self.dropdown_kamera.bind("<Button-1>", lambda e: self.toggle_dropdown())
        self.dropdown_kamera.bind("<Enter>", self.hover)
        
        self.count_kamera = len(kamera_list)
        self.kamera_dict = {i: v for i, v in enumerate(kamera_list)}
        self.listbox = tk.Listbox(self, font=("Arial", 12, "bold"))
        for item in kamera_list:
            self.listbox.insert(tk.END, item)

        self.listbox.bind("<<ListboxSelect>>", self.pilih)
        self.listbox.bind("<Enter>", self.hover)
        
        judul2 = tk.Label(self, text="Orientation", bg="#add8e6", font=("Arial", title_size, "bold"))
        judul2.place(relx=0.14, rely=0.4, anchor="w")
        
        self.buat_radio_canvas()
        
        judul3 = tk.Label(self, text="Time", bg="#add8e6", font=("Arial", title_size, "bold"))
        judul3.place(relx=0.14, rely=0.6, anchor="w")

    # Kalau udah ada settings.ini diubah
    camera = 0
    orientation = 0
    time = 0
    
    @property
    def camera_setting(self):
        return self.camera
    
    @camera_setting.setter
    def camera_setting(self, index):
        self.camera = index
    
    @property
    def orientation_setting(self):
        return self.orientation
    
    @orientation_setting.setter
    def orientation_setting(self, index):
        self.orientation = index
    
    @property
    def time_setting(self):
        return self.time
    
    @time_setting.setter
    def time_setting(waktu, self):
        self.time = waktu
    
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

    def toggle_dropdown(self):
        if self.listbox.winfo_ismapped():
            self.listbox.place_forget()
            self.unbind_all("<Button-1>")
        else:
            self.listbox.place(relx=0.17, rely=0.29, relwidth=0.7, relheight=0.038*self.count_kamera)
            self.listbox.lift()
            self.after(100, lambda: self.bind_all("<Button-1>", self.on_global_click))

    def on_global_click(self, event):
        widget = event.widget
        if widget != self.listbox and widget != self.dropdown_kamera:
            self.listbox.place_forget()
            self.unbind_all("<Button-1>")
    
    def pilih(self, e):
        pilihan = self.listbox.get(self.listbox.curselection())
        self.pilihan.set(pilihan)
        self.dropdown_kamera.config(text="▼  " + pilihan)
        self.listbox.place_forget()
        self.camera_setting = [k for k, v in self.kamera_dict.items() if v == pilihan][0]
    
    def buat_radio_canvas(self):
        opsi = [("Landscape", 0), ("Portrait", 1)]
        # Kalau udah ada settings.ini diubah
        self.orientation_var = tk.StringVar(value=self.orientation)
        self.orientation_items = []

        for i, (text, value) in enumerate(opsi):
            x_pos = 0.17 + (0.25 * i)

            # Canvas lingkaran
            canvas = tk.Canvas(self, width=40, height=40, bg="#add8e6", highlightthickness=0)
            canvas.place(relx=x_pos, rely=0.48, anchor="w")
            canvas.bind("<Enter>", self.hover)

            lingkaran = canvas.create_oval(5, 5, 35, 35, outline="black", width=2)
            titik = canvas.create_oval(13, 13, 27, 27, fill="", width=0)

            # Label teks di sebelah kanan lingkaran
            label = tk.Label(self, text=text, bg="#add8e6", font=("Arial", 12, "bold"))
            label.place(relx=x_pos + 0.05, rely=0.485, anchor="w")  # Geser dikit ke kanan
            label.bind("<Enter>", self.hover)

            def on_click(e=None, v=value, c=canvas, t=titik):
                self.orientation_var.set(v)
                for _, can, ti in self.orientation_items:
                    can.itemconfig(ti, fill="")
                c.itemconfig(t, fill="black")
                self.orientation_setting = v

            canvas.bind("<Button-1>", on_click)
            label.bind("<Button-1>", on_click)
            self.orientation_items.append((value, canvas, titik))

        # Set default aktif
        self.orientation_var.set(self.orientation)
        self.orientation_items[self.orientation][1].itemconfig(self.orientation_items[self.orientation][2], fill="black")
