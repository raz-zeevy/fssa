from customtkinter import *
from PIL import Image
from lib.utils import *
import ttkbootstrap as ttk
from lib.components.form import HelpButton
from tktooltip import ToolTip

MAIN_BTN_FOREGROUND = "#325d88"
MAIN_BTN_FOCUSED = "#325d88"

SECONDARY_FOCUS_COLOR = "#40aff1"

class StartPage(ttk.Frame):
    def __init__(self, parent):
        self.root = parent.root
        ttk.Frame.__init__(self, parent.root)
        self.colors = parent.root.style.colors
        self.create_widgets()
        self.root.update()

    def create_widgets(self):
        side_img_data = Image.open(get_resource("side-img5.png"))
        side_img = CTkImage(dark_image=side_img_data,
                            light_image=side_img_data,
                            size=(WINDOW_WIDTH/2,WINDOW_HEIGHT))

        CTkLabel(master=self, text="", image=side_img).pack(expand=True,
                                                           side="left")
        frame = CTkFrame(master=self, width=300, height=480,
                         fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")

        CTkLabel(master=frame, text="FSSA", text_color="#601E88", anchor="w",
                 justify="left", font=("Arial Bold", 24)).pack(anchor="w",
                                                               pady=(50, 0),
                                                               padx=(25, 0))
        # create another sub title just below the FSSA with this text:
        # Faceted Smallest Space Analysis for Windows"
        CTkLabel(master=frame, text="Faceted Smallest Space Analysis for "
                                    "Windows", text_color="#7E7E7E", anchor="w",
                    justify="left", font=("Arial Bold", 14),
                 wraplength=250).pack(anchor="w",padx=(25, 0),pady=(0, 20))
        CTkLabel(master=frame,
                 text="Chose the type of input file you wish\nto "
                      "process.", text_color="#7E7E7E", anchor="w",
                 justify="left", font=("Arial Bold", 12)).pack(anchor="w",
                                                               padx=(25, 0))
        #
        self.button_recorded_data = CTkButton(master=frame, text="Recorded "
                                                               "Data",
                         fg_color="#601E88",
                  hover_color="#E44982", font=("Arial Bold", 12),
                  text_color="#ffffff", width=225,)
        self.button_recorded_data.pack(anchor="w",
                                       padx=(19, 0),
                                       pady=(38, 0))
        ToolTip(self.button_recorded_data, msg="Press here if your input file "
                                        "consists of a list of cases (e.g., "
                                        "subjects), that\n are scored with "
                                        "respect to a set of variables to be "
                                        "mapped by FSSA.",
                delay=0)
        self.button_matrix_data = CTkButton(master=frame,
                                            text="Dis/similarity Matrix",
                           fg_color="#601E88",
                  hover_color="#E44982", font=("Arial Bold", 12),
                  text_color="#ffffff", width=225,)
        self.button_matrix_data.pack(anchor="w",
                                     padx=(19,0),
                                     pady=(38,0))
        ToolTip(self.button_matrix_data, msg="Press here if your input file "
                                        "consists of a symmetric matrix of "
                                        "similarity coefficients (e.g., "
                                        "correlations) or dissimilarity "
                                        "coefficients (distances) between "
                                        "objects to be mapped by FSSA.",
                delay=0)
        self.button_info = CTkButton(master=frame, text="What is FSSA?",
                  fg_color=self.colors.primary,
                  hover_color=SECONDARY_FOCUS_COLOR, font=("Arial Bold", 12),
                  text_color="#ffffff", width=225)
        self.button_info.pack(anchor="w",
                                                        padx=(25, 0),
                                                        pady=(150, 0))