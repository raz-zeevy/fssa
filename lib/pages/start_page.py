from customtkinter import *
from PIL import Image
from lib.utils import *
import ttkbootstrap as ttk

class StartPage(ttk.Frame):
    def __init__(self, parent):
        self.root = parent.root
        ttk.Frame.__init__(self, parent.root)
        self.colors = parent.root.style.colors
        self.create_widgets()
        parent.root.geometry("930x740")

    def create_widgets(self):
        side_img_data = Image.open(get_resource("side-img.png"))

        side_img = CTkImage(dark_image=side_img_data,
                            light_image=side_img_data, size=(320, 493))

        CTkLabel(master=self, text="", image=side_img).pack(expand=True,
                                                           side="left")

        frame = CTkFrame(master=self, width=300, height=480,
                         fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")

        CTkLabel(master=frame, text="FSSA", text_color="#601E88", anchor="w",
                 justify="left", font=("Arial Bold", 24)).pack(anchor="w",
                                                               pady=(50, 5),
                                                               padx=(25, 0))
        CTkLabel(master=frame,
                 text="Chose the type of input file you wish\nto "
                      "process.", text_color="#7E7E7E", anchor="w",
                 justify="left", font=("Arial Bold", 12)).pack(anchor="w",
                                                               padx=(25, 0))

        self.button_recorded_data = CTkButton(master=frame, text="Recorded "
                                                               "Data",
                         fg_color="#601E88",
                  hover_color="#E44982", font=("Arial Bold", 12),
                  text_color="#ffffff", width=225)
        self.button_recorded_data.pack(anchor="w",padx=(25, 0),
                                                        pady=(38, 0))

        self.button_matrix_data = CTkButton(master=frame, text="Matrix Data",
                           fg_color="#601E88",
                  hover_color="#E44982", font=("Arial Bold", 12),
                  text_color="#ffffff", width=225)

        self.button_matrix_data.pack(anchor="w",
                                                        padx=(25, 0),
                                                        pady=(38, 0))

        self.button_info = CTkButton(master=frame, text="What is FSSA?",
                  fg_color=self.colors.primary,
                  hover_color="#E44982", font=("Arial Bold", 12),
                  text_color="#ffffff", width=225)
        self.button_info.pack(anchor="w",
                                                        padx=(25, 0),
                                                        pady=(150, 0))