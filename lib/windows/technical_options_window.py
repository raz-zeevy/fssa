import os
import ttkbootstrap as ttk
import tkinter as tk
from lib.moduls.help_content import *
from lib.windows.window import Window
from lib.utils import *
from lib.components.form import *

class TOWindow(Window):
    def __init__(self, parent, locality : list, **kwargs):
        """
        """
        self.locality = locality
        super().__init__(**kwargs, geometry="600x175")
        self.title("Technical Options")
        self.iconbitmap(get_resource("icon.ico"))
        # sets the geometry of toplevel
        self.center_window()
        # init
        self.create_entries()
        self.create_help()
        self.create_buttons()
        self.bind("<Escape>", lambda x: self.exit())


    def center_window(self):
        self.update_idletasks()  # Update "requested size" from geometry manager
        # Calculate x and y coordinates for the Tk root window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = (screen_width / 2) - (size[0] / 2)
        y = 0
        self.geometry("+%d+%d" % (x, y))

    def create_help(self):
        # Status Bar
        status_bar = ttk.Label(self, text="For Help, press F1",
                               relief=ttk.SUNKEN, anchor='w')
        # pack the status bar at the bottom of the screen
        status_bar.pack(side=ttk.BOTTOM, fill='x')

    def create_entries(self):
        locality_frame = ttk.Frame(self)
        locality_frame.pack(side=tk.TOP, fill='x', padx=10, pady=(20,0))
        self.locality_label = ttk.Label(locality_frame,
                                        text="What is the weight for "
                                             "locality? (-5 to +5)",
                                        wraplength=400, justify="left")
        self.locality_label.pack(side=tk.LEFT, padx=5, fill="x")
        grouping_values = [str(i) for i in range(-5,6)]
        self.locality_entry = SelectionBox(locality_frame,
                                           values=grouping_values,
                                           default=str(self.locality[0]),
                                           width=5, )
        self.locality_entry.pack(side=tk.RIGHT, padx=(0, 20), pady=(10, 0))

    def create_buttons(self):
        # create "Recode" and "Cancle" buttons in the center bottom of the
        # screen
        frame_buttons = ttk.Frame(self)
        frame_buttons.pack(side=tk.BOTTOM, fill='x', padx=(165,50), pady=(0,
                                                                          20))
        self.button_cancel = NavigationButton(frame_buttons, text="Cancel",
                                              bootstyle="secondary",
                                        command=self.exit)
        self.button_cancel.pack(side=tk.LEFT, padx=5)
        self.button_ok = NavigationButton(frame_buttons, text="Ok",
                                        command=lambda : self.ok_pressed())
        self.button_ok.pack(side=tk.LEFT, padx=30)

    #####################
    # Getters & Setters #
    #####################

    def get_locality(self):
        return self.locality_entry.get()

    def set_locality(self, value):
        self.locality_entry.set(value)

    ###########
    # Methods #
    ###########

    def ok_pressed(self):
        self.locality[0] = self.get_locality()
        self.exit()

    def exit(self):
        self.destroy()
