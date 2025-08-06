class Style():
    def center_window(window, width, height):
        """Memusatkan jendela Tkinter pada layar."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_coordinate = (screen_width/2) - (width/2)
        y_coordinate = (screen_height/2) - (height/2)
        window.geometry(f"{width}x{height}+{int(x_coordinate)}+{int(y_coordinate)}")