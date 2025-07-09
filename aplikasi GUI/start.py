import tkinter as tk
import cv2
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Hentikan logging absl (Google logging framework yg dipakai TF)
import logging
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)
logging.getLogger('tensorflow').setLevel(logging.ERROR)

import tensorflow as tf
import time
import pygame
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime
from assets.helper.get_resource import resource_path
from assets.helper.get_camera import get_camera
from assets.helper.save_settings import load_settings
from assets.helper.get_time import get_salat_time
from assets.helper.check import check_true

class Start(tk.Frame):

    def __init__(self, parent, show_next, model_predictor):
        super().__init__(parent)
        self.show_next = show_next
        pygame.mixer.init()
        self.configure(bg="lightblue")
        self.cap = None
        self.model_predictor = model_predictor
        self.build_ui()

    def build_ui(self):
        my_bg = "lightblue"
        
        image_width = 75
        image_height = 50
        
        settings = load_settings()
        
        img = Image.open(resource_path("assets/images/arrow.png")).resize((image_width, image_height), Image.LANCZOS)
        self.back_img = ImageTk.PhotoImage(img)
        
        img = Image.open(resource_path("assets/images/arrow_hover.png")).resize((image_width, image_height), Image.LANCZOS)
        self.back_hover_img = ImageTk.PhotoImage(img)
        
        self.label_back = tk.Label(self, image=self.back_img, bg=my_bg, borderwidth=0)
        self.label_back.place(relx=0.01, rely=0.01, anchor="nw")
        self.label_back.bind("<Button-1>", self.back)
        self.label_back.bind("<Enter>", self.on_enter)
        self.label_back.bind("<Leave>", self.on_leave)
        
        jam_atas_frame = tk.Frame(self, bg=my_bg)
        jam_atas_frame.place(relx=1, rely=0.0, anchor="ne")

        jam_frame = tk.Frame(jam_atas_frame, bg=my_bg)
        jam_frame.pack(side="top")
        
        self.label_hour = tk.Label(jam_frame, text="--", font=("Arial", 20, "bold"), bg=my_bg)
        self.label_colon = tk.Label(jam_frame, text=":", font=("Arial", 20, "bold"), bg=my_bg)
        self.label_minute = tk.Label(jam_frame, text="--", font=("Arial", 20, "bold"), bg=my_bg)
        
        self.start_time = datetime.strptime(settings["time"], "%H:%M")
        self.run_start = datetime.now()
        
        self.label_hour.pack(side="left")
        self.label_colon.pack(side="left")
        self.label_minute.pack(side="left")
        
        self.visible = True
        self.update_time()
        self.blink_colon()

        judul = tk.Label(jam_atas_frame, text=get_salat_time(settings["time"]), bg=my_bg, font=("Arial", 14, "bold"))
        judul.pack(side="right")

        self.salah = tk.Label(self, text="Teridentifikasi Salah", bg=my_bg, font=("Arial", 14, "bold"), fg="red")
        
        self.frame_mid = tk.Frame(self, bg="black")
        self.frame_mid.place(relx=0.5, rely=0.48, relwidth=0.55, relheight=0.8, anchor="center")
        
        self.cam = tk.Label(self.frame_mid)
        
        frame_set = tk.Frame(self, bg=my_bg)
        frame_set.place(relx=0.2, rely=0.92, relheight=0.2, relwidth=0.6, anchor="nw")
        
        frame_set.rowconfigure(0, weight=0)
        frame_set.columnconfigure(0, weight=1)
        frame_set.columnconfigure(1, weight=2)
        frame_set.columnconfigure(2, weight=2)
        frame_set.columnconfigure(3, weight=1) 
        
        spacer = tk.Label(frame_set, bg=my_bg)
        spacer.grid(row=0, column=0, sticky="nsew")
        
        kamera_list = get_camera()
        
        kamera_default = self.camera
        self.pilihan = tk.StringVar(value=kamera_list[kamera_default])
        
        self.dropdown_kamera = tk.Label(frame_set, text="▲  " + self.pilihan.get(), font=("Arial", 14, "bold"), anchor="w", borderwidth=2, relief="solid")
        self.dropdown_kamera.grid(row=0, column=1, sticky="nsew")
        self.dropdown_kamera.bind("<Button-1>", lambda e: self.toggle_dropdown())
        self.dropdown_kamera.bind("<Enter>", self.hover)
        
        self.count_kamera = len(kamera_list)
        self.kamera_dict = {i: v for i, v in enumerate(kamera_list)}
        self.listbox = tk.Listbox(self, font=("Arial", 12, "bold"), height=self.count_kamera)
        for item in kamera_list:
            self.listbox.insert(tk.END, item)
        
        self.listbox.bind("<<ListboxSelect>>", self.pilih)
        self.listbox.bind("<Enter>", self.hover)
        
        orientation = ["Landscape", "Portrait"]
        orientation_set = settings["orientation"]
        self.orientation_dict = {i: v for i, v in enumerate(orientation)}
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
        
        spacer1 = tk.Label(frame_set, bg=my_bg)
        spacer1.grid(row=0, column=3, sticky="nsew")
        
        frame_log = tk.Frame(self)
        frame_log.place(relx=0, rely=1, relwidth=0.2, relheight=0.04, anchor="sw")
        
        self.dropdown_log = tk.Label(frame_log, text="▲  Open Log", bg="black", fg="white", font=("Arial", 16, "bold"))
        self.dropdown_log.pack(side="bottom", fill="x")
        self.dropdown_log.bind("<Button-1>", lambda e: self.toggle_dropdown_log())
        self.dropdown_log.bind("<Enter>", self.hover)
        
        self.scrollbar = tk.Scrollbar(self)
        
        self.logbox = tk.Text(self, wrap="char", yscrollcommand=self.scrollbar.set, font=("Arial", 10, "bold"), fg="white", bg="black")
        self.logbox.bind("<Button-1>", lambda e: "break")
        self.logbox.bind("<<ListboxSelect>>", lambda e: "break")
        self.logbox.tag_configure("indented", lmargin1=5, lmargin2=117)
        
        self.scrollbar.config(command=self.logbox.yview)
        
        self.update_frame()


    settings = load_settings()
    camera = settings["camera"]
    orientation = settings["orientation"]
    time = settings["time"]
    salat_time = get_salat_time(time)
    
    _runtutan = []
    _gerak_curr = ""
    _rakaat_now = 0

    kebenaran = False
    nampak = True
    salah_first = True
    transisi = False
    rukun = 1
    mulai = True
    yakin = False
    
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
    def runtutan(self):
        return self._runtutan
    
    @runtutan.setter
    def runtutan(self, array):
        self._runtutan = array
    
    @property
    def gerak_curr(self):
        return self._gerak_curr
    
    @gerak_curr.setter
    def gerak_curr(self, value):
        self._gerak_curr = value
    
    @property
    def rakaat_now(self):
        return self._rakaat_now
    
    @rakaat_now.setter
    def rakaat_now(self, index):
        self._rakaat_now = index
    
    def back(self, e):
        self.show_next("homepage")
        self.log("Kamera dimatikan")
        self.cap.release()

    def on_enter(self, e):
        self.label_back.config(image=self.back_hover_img)
        e.widget.config(cursor="hand2")

    def hover(self, e):
        e.widget.config(cursor="hand2")
    
    def on_leave(self, e):
        self.label_back.config(image=self.back_img)
        e.widget.config(cursor="")
    
    def update_time(self):
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
            self.listbox.place(relx=0.27, rely=0.92, relwidth=0.27, anchor="sw")
            self.listbox.lift()
            self.after(1000, lambda: self.bind_all("<Button-1>", self.on_global_click))
    
    def on_global_click(self, event):
        widget = event.widget
        if widget != self.listbox and widget != self.dropdown_kamera:
            self.listbox.place_forget()
            self.unbind_all("<Button-1>")
    
    def pilih(self, e):
        if self.listbox.curselection():
            pilihan = self.listbox.get(self.listbox.curselection())
            camera = [k for k, v in self.kamera_dict.items() if v == pilihan][0]
            self.pilihan.set(pilihan)
            self.camera_setting = camera
            self.dropdown_kamera.config(text="▲  " + pilihan)
            self.listbox.place_forget()
            self.log(f"Kamera berganti menjadi {pilihan}")
            
            self.stop_camera()
            self.start_camera(self.camera_setting, False)
    
    def toggle_dropdown_orientation(self):
        if self.listbox_orientation.winfo_ismapped():
            self.listbox_orientation.place_forget()
            self.unbind_all("<Button-1>")
        else:
            self.listbox_orientation.place(relx=0.57, rely=0.92, relwidth=0.12, anchor="sw")
            self.listbox_orientation.lift()
            self.after(1000, lambda: self.bind_all("<Button-1>", self.on_global_click_orientation))
    
    def on_global_click_orientation(self, event):
        widget = event.widget
        if widget != self.listbox_orientation and widget != self.dropdown_orientation:
            self.listbox_orientation.place_forget()
            self.unbind_all("<Button-1>")
    
    def pilih_orientation(self, e):
        if self.listbox_orientation.curselection():
            pilihan = self.listbox_orientation.get(self.listbox_orientation.curselection())
            orientation = [k for k, v in self.orientation_dict.items() if v == pilihan][0]
            self.pilihan_orientation.set(pilihan)
            self.dropdown_orientation.config(text="▲  " + pilihan)
            self.listbox_orientation.place_forget()
            self.orientation_setting = orientation
            
            self.cam.place_forget()
            
            if self.orientation_setting == 0:
                self.cam.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=0.75)
            else:
                self.cam.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.75, relheight=1)
    
    def toggle_dropdown_log(self):
        if self.logbox.winfo_ismapped():
            self.logbox.place_forget()
            self.unbind_all("<Button-1>")
        else:
            self.logbox.place(relx=0, rely=0.96, relwidth=0.5, relheight=0.8, anchor="sw")
            self.logbox.lift()
            self.after(100, lambda: self.bind_all("<Button-1>", self.on_global_click_log))
    
    def on_global_click_log(self, event):
        widget = event.widget
        if widget != self.dropdown_log:
            self.logbox.place_forget()
            self.unbind_all("<Button-1>")
    
    def log(self, text):
        file_log = resource_path("assets/log.txt")
        
        log = f"[{datetime.now().strftime("%d-%m-%Y %H:%M")}] {text}\n"
        
        with open(file_log, mode="a") as file:
            file.write(log)
            
        self.logbox.insert(tk.END, log,  "indented")
        self.logbox.insert(tk.END, "\n",  "indented")
        self.logbox.yview_moveto(1.0)
    
    def start_camera(self, camera, first_time):
        if first_time:
            self.log("Kamera dihidupkan")
        
        if self.orientation_setting == 0:
            self.cam.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=0.75)
        else:
            self.cam.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.75, relheight=1)
        
        self.cap = cv2.VideoCapture(camera)
        self.running = True
        self.update_frame()

    def stop_camera(self):
        if self.cap.isOpened():
            self.cap.release()
    
    def process_input(self, image):
        img = tf.image.resize_with_pad(tf.expand_dims(image, axis=0), 256, 256)
        return tf.cast(img, dtype=tf.int32)
    
    def update_frame(self):
        if not self.cap:
            return

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            input_image = self.process_input(frame)
            
            gerakan = ["berdiri", "duduk", "ruku", "sujud"]
            prediksi, teridentifikasi = self.model_predictor.get_predict(input_image)

            if teridentifikasi and self.nampak:
                self.log("Objek teridentifikasi!")
                self.nampak = False
            
            if self.rukun == 1:
                trans = [3, 6]
            elif self.rukun == 2:
                trans = [3, 6, 7]
            elif self.rukun == 3:
                trans = [3]
            else:
                trans = []
            
            if len(prediksi[0]) > 1 and np.max(prediksi) > 0.79:
                label_index = np.argmax(prediksi)
                print(f"Terdeteksi : {gerakan[label_index]}")
                if len(self.runtutan) in trans:
                    self.transisi = True
                else:
                    self.transisi = False
                if len(self.runtutan) < 2:
                    if  len(self.runtutan) == 0 and gerakan[label_index] == "berdiri":
                        self.runtutan = ["berdiri"]
                        self.gerak_curr = "berdiri"
                        self.log("Objek teridentifikasi melakukan gerakan berdiri")
                    elif len(self.runtutan) == 1 and gerakan[label_index] == "ruku":
                        self.runtutan += ["ruku"]
                        self.gerak_curr = "ruku"
                        if self.mulai:
                            self.log(f"Objek teridentifikasi melakukan ruku setelah berdiri, pertanda melaksanakan salat {self.salat_time}")
                            self.mulai = False
                        else:
                            self.log("Objek teridentifikasi melakukan gerakan ruku")
                else:
                    print(f"Gerak terdeteksi : {gerakan[label_index]}")
                    print(f"Yakin : {self.yakin}")
                    print(f"Runtutan : {self.runtutan}")
                    print("END")
                    if not self.runtutan[-1] == gerakan[label_index]:
                        rakaat, runtut, kebenaran, curr, next, cetak, cetak2, rukunn = check_true(self.salat_time, gerakan[label_index], self.rakaat_now, self.runtutan, self.gerak_curr)
                        self.rakaat_now = rakaat
                        self.runtutan = runtut
                        self.gerak_curr = curr
                        self.kebenaran = kebenaran
                        self.rukun = rukunn

                        if not self.transisi:
                            if cetak:
                                self.log(f"Objek teridentifikasi melakukan {gerakan[label_index]}")
                            if cetak2:
                                self.log(f"Objek teridentifikasi telah menyelesaikan rakaat ke-{self.rakaat_now} pada salat {self.salat_time}")
                            if not self.kebenaran:
                                if self.yakin:
                                    file_path = resource_path("assets/helper/subhanallah.mp3")
                                    pygame.mixer.music.load(file_path)
                                    pygame.mixer.music.play()
                                    self.log(f"Objek teridentifikasi melakukan kesalahan pada rakaat ke-{self.rakaat_now+1}, yaitu gerakan {next} teridentifikasi {gerakan[label_index]}")
                                    self.yakin = False
                                else:
                                    time.sleep(1.5)
                                    self.yakin = True
                            else:
                                self.yakin = False
                        else:
                            if self.yakin and self.kebenaran:
                                if cetak:
                                    self.log(f"Objek teridentifikasi melakukan {gerakan[label_index]}")
                                if cetak2:
                                    self.log(f"Objek teridentifikasi telah menyelesaikan rakaat ke-{self.rakaat_now} pada salat {self.salat_time}")
                                self.yakin = False
                            elif self.yakin and not self.kebenaran:
                                file_path = resource_path("assets/helper/subhanallah.mp3")
                                pygame.mixer.music.load(file_path)
                                pygame.mixer.music.play()
                                self.log(f"Objek teridentifikasi melakukan kesalahan pada rakaat ke-{self.rakaat_now+1}, yaitu gerakan {next} teridentifikasi {gerakan[label_index]}")
                                self.yakin = False
                            elif not self.yakin:
                                print(f"Padahal yakinnya {self.yakin}, tapi masuk")
                                if self.kebenaran and len(self.runtutan) > 1:
                                    self.runtutan.pop()
                                self.yakin = True
                                time.sleep(3.8)
            
            # Ambil ukuran aktual dari self.cam
            cam_width = self.cam.winfo_width()
            cam_height = self.cam.winfo_height()

            # Jika ukuran belum terbaca (di awal biasanya 1x1), beri default
            if cam_width <= 1 or cam_height <= 1:
                cam_width, cam_height = 640, 480

            # Resize frame ke ukuran tampilan
            resized_frame = cv2.resize(frame, (cam_width, cam_height))

            img = Image.fromarray(resized_frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.cam.imgtk = imgtk
            self.cam.config(image=imgtk)

        self.cam.after(50, self.update_frame) # 60fps
    
    def on_close(self):
        self.log("Kamera dimatikan")
        self.cap.release()