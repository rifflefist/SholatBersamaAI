import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from assets.helper.get_resource import resource_path
from assets.helper.get_camera import get_camera
from assets.helper.get_time import get_time
from assets.helper.save_settings import save_settings
from assets.helper.save_settings import load_settings

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
        
        self.dropdown_kamera = tk.Label(self, text="▼  " + self.pilihan.get(), font=("Arial", 14, "bold"), anchor="w")
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
        
        self.set_auto = tk.IntVar()  # Untuk menyimpan status checkbox (0 atau 1)

        checkbox = tk.Checkbutton(self, text="Set Automatically", bg="#add8e6",font=("Arial", 12, "bold"), variable=self.set_auto, command=self.toggle_button_set_auto)
        checkbox.place(relx=0.17, rely=0.67, anchor="w", relheight=0.05)
        
        label_time_set = tk.Label(self, text="Set Manual", bg="#add8e6", font=("Arial", 12, "bold"))
        label_time_set.place(relx=0.17, rely=0.74, anchor="w")
        
        jam, menit = self.time_setting.split(":")
        self.pilihan_hour = tk.StringVar(value=jam)
        
        self.dropdown_hour = tk.Label(self, text=""+self.pilihan_hour.get(), font=("Arial", 14, "bold"), anchor="center")
        self.dropdown_hour.place(relx=0.3, rely=0.74, anchor="w")
        self.dropdown_hour.bind("<Button-1>", lambda e: self.toggle_dropdown_hour())
        self.dropdown_hour.config(cursor="hand2")
        
        self.listbox_hour = tk.Listbox(self, font=("Arial", 12, "bold"))
        for i in range(0, 24):
            if i < 10:
                i = "0"+str(i)
            else:
                i = str(i)
            self.listbox_hour.insert(tk.END, str(i))
        
        self.listbox_hour.bind("<<ListboxSelect>>", self.pilih_hour)
        self.listbox_hour.bind("<Enter>", self.hover)
        
        scroll_hour = tk.Scrollbar(self, orient="vertical", command=self.listbox_hour.yview)
        self.listbox_hour.config(yscrollcommand=scroll_hour.set)
        
        pemisah_waktu = tk.Label(self, text=":", bg="#add8e6", font=("Arial", 16, "bold"))
        pemisah_waktu.place(relx=0.335, rely=0.74, anchor="w")
        
        self.pilihan_min = tk.StringVar(value=menit)
        
        self.dropdown_min = tk.Label(self, text=""+self.pilihan_min.get(), font=("Arial", 14, "bold"), anchor="center")
        self.dropdown_min.place(relx=0.36, rely=0.74, anchor="w")
        self.dropdown_min.bind("<Button-1>", lambda e: self.toggle_dropdown_min())
        self.dropdown_min.config(cursor="hand2")
        
        self.listbox_min = tk.Listbox(self, font=("Arial", 12, "bold"))
        for i in range(0, 60):
            if i < 10:
                i = "0"+str(i)
            else:
                i = str(i)
            self.listbox_min.insert(tk.END, str(i))
        
        self.listbox_min.bind("<<ListboxSelect>>", self.pilih_min)
        self.listbox_min.bind("<Enter>", self.hover)
        
        scroll_min = tk.Scrollbar(self, orient="vertical", command=self.listbox_min.yview)
        self.listbox_min.config(yscrollcommand=scroll_min.set)
        
        my_label = tk.Label(self, text="github.com/rifflefist", font=("Arial", 10, "bold"), bg="#add8e6")
        my_label.place(relx=0.99, rely=0.99, anchor="se")

    settings = load_settings()
    # Kalau udah ada settings.ini diubah
    camera = settings["camera"]
    orientation = settings["orientation"]
    time = settings["time"]
    
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
    def time_setting(self, waktu):
        self.time = waktu
    
    def back(self, e):
        if self.camera_setting != self.settings["camera"] or self.orientation_setting != self.settings["orientation"] or self.time_setting != self.settings["time"]:
            hasil =  messagebox.askyesno("Warning", "Do you want to save the changes?")
            if hasil:
                save_settings(self.camera_setting, self.orientation_setting, self.time_setting)
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
            
    def toggle_dropdown_hour(self):
        if not self.set_auto.get():
            if self.listbox_hour.winfo_ismapped():
                self.listbox_hour.place_forget()
                self.unbind_all("<Button-1>")
            else:
                self.listbox_hour.place(relx=0.3, rely=0.76, anchor="nw", relwidth=0.04, relheight=0.2)
                self.listbox_hour.lift()
                self.after(100, lambda: self.bind_all("<Button-1>", self.on_global_click_hour))
    
    def toggle_dropdown_min(self):
        if not self.set_auto.get():
            if self.listbox_min.winfo_ismapped():
                self.listbox_min.place_forget()
                self.unbind_all("<Button-1>")
            else:
                self.listbox_min.place(relx=0.36, rely=0.76, anchor="nw", relwidth=0.04, relheight=0.2)
                self.listbox_min.lift()
                self.after(100, lambda: self.bind_all("<Button-1>", self.on_global_click_min))

    def on_global_click(self, event):
        widget = event.widget
        if widget != self.listbox and widget != self.dropdown_kamera:
            self.listbox.place_forget()
            self.unbind_all("<Button-1>")
    
    def on_global_click_hour(self, event):
        widget = event.widget
        if widget != self.listbox_hour and widget != self.dropdown_hour:
            self.listbox_hour.place_forget()
            self.unbind_all("<Button-1>")
    
    def on_global_click_min(self, event):
        widget = event.widget
        if widget != self.listbox_min and widget != self.dropdown_min:
            self.listbox_min.place_forget()
            self.unbind_all("<Button-1>")
    
    def pilih(self, e):
        if self.listbox.curselection():
            pilihan = self.listbox.get(self.listbox.curselection())
            self.pilihan.set(pilihan)
            self.dropdown_kamera.config(text="▼  " + pilihan)
            self.listbox.place_forget()
            self.camera_setting = [k for k, v in self.kamera_dict.items() if v == pilihan][0]
    
    def pilih_hour(self, e):
        if self.listbox_hour.curselection():
            pilihan_hour = self.listbox_hour.get(self.listbox_hour.curselection())
            self.pilihan_hour.set(pilihan_hour)
            _, min = self.time_setting.split(":")
            self.time_setting = f"{pilihan_hour}:{min}"
            self.dropdown_hour.config(text=pilihan_hour)
            self.listbox_hour.place_forget()
    
    def pilih_min(self, e):
        if self.listbox_min.curselection():
            pilihan_min = self.listbox_min.get(self.listbox_min.curselection())
            self.pilihan_min.set(pilihan_min)
            hour, _ = self.time_setting.split(":")
            self.time_setting = f"{hour}:{pilihan_min}"
            self.dropdown_min.config(text=pilihan_min)
            self.listbox_min.place_forget()
    
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
    
    def toggle_button_set_auto(self):
        hour, min = get_time()
        self.time_setting = f"{hour}:{min}"
        if self.set_auto.get():
            self.dropdown_hour.config(text=hour, state="disabled", cursor="arrow")
            self.dropdown_min.config(text=min, state="disabled", cursor="arrow")
        else:
            self.dropdown_hour.config(state="normal", cursor="hand2")
            self.dropdown_min.config(state="normal", cursor="hand2")
