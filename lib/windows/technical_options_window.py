import os
import ttkbootstrap as ttk
import tkinter as tk
from lib.moduls.help_content import *
from lib.windows.window import Window
from lib.utils import *
from lib.components.form import *

class TOWindow(Window):
    def __init__(self, parent, locality : list, formfeed : list, diagram_chars : list, trimmed_ascii : list, **kwargs):
        """
        """
        self.locality = locality
        self.formfeed = formfeed
        self.diagram_chars = diagram_chars
        self.trimmed_ascii = trimmed_ascii
        super().__init__(**kwargs, geometry="600x300")
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
        # Locality frame
        locality_frame = ttk.Frame(self)
        locality_frame.pack(side=tk.TOP, fill='x', padx=10, pady=(20,10))
        self.locality_label = ttk.Label(locality_frame,
                                        text="What is the weight for "
                                             "locality? (-5 thru +5)",
                                        wraplength=400, justify="left")
        self.locality_label.pack(side=tk.LEFT, padx=5, fill="x")
        grouping_values = [str(i) for i in range(-5,6)]
        self.locality_entry = SelectionBox(locality_frame,
                                           values=grouping_values,
                                           default=str(self.locality[0]),
                                           width=5, )
        self.locality_entry.pack(side=tk.RIGHT, padx=(0, 20), pady=(10, 0))

        # FORMFEED character frame
        formfeed_frame = ttk.Frame(self)
        formfeed_frame.pack(side=tk.TOP, fill='x', padx=10, pady=(0,10))
        self.formfeed_label = ttk.Label(formfeed_frame,
                                        text="Enter special FORMFEED character if needed for printer.",
                                        wraplength=400, justify="left")
        self.formfeed_label.pack(side=tk.LEFT, padx=5, fill="x")
        self.formfeed_entry = ttk.Entry(formfeed_frame, width=10)
        self.formfeed_entry.pack(side=tk.RIGHT, padx=(0, 20), pady=(10, 0))
        if self.formfeed[0]:
            self.formfeed_entry.insert(0, self.formfeed[0])

        # Diagram-frame characters frame
        diagram_frame = ttk.Frame(self)
        diagram_frame.pack(side=tk.TOP, fill='x', padx=10, pady=(0,10))
        self.diagram_label = ttk.Label(diagram_frame,
                                       text="To change diagram-frame characters, enter eight chars:",
                                       wraplength=400, justify="left")
        self.diagram_label.pack(side=tk.LEFT, padx=5, fill="x")
        self.diagram_entry = ttk.Entry(diagram_frame, width=10)
        self.diagram_entry.pack(side=tk.RIGHT, padx=(0, 20), pady=(10, 0))
        if self.diagram_chars[0]:
            self.diagram_entry.insert(0, self.diagram_chars[0])

        # Trimmed ASCII output frame
        ascii_frame = ttk.Frame(self)
        ascii_frame.pack(side=tk.TOP, fill='x', padx=10, pady=(0,10))
        self.ascii_label = ttk.Label(ascii_frame,
                                     text="Do you want a trimmed ASCII output file to be written ?",
                                     wraplength=400, justify="left")
        self.ascii_label.pack(side=tk.LEFT, padx=5, fill="x")
        ascii_values = ["Yes", "No"]
        self.ascii_entry = SelectionBox(ascii_frame,
                                        values=ascii_values,
                                        default=self.trimmed_ascii[0],
                                        width=5)
        self.ascii_entry.pack(side=tk.RIGHT, padx=(0, 20), pady=(10, 0))

    def create_buttons(self):
        # create "OK" and "Cancel" buttons in the center bottom of the screen
        frame_buttons = ttk.Frame(self)
        frame_buttons.pack(side=tk.BOTTOM, fill='x', padx=(165,50), pady=(0, 20))

        self.button_ok = NavigationButton(frame_buttons, text="OK",
                                        command=lambda : self.ok_pressed())
        self.button_ok.pack(side=tk.LEFT, padx=5)

        self.button_cancel = NavigationButton(frame_buttons, text="Cancel",
                                              bootstyle="secondary",
                                        command=self.exit)
        self.button_cancel.pack(side=tk.LEFT, padx=30)

        self.button_help = NavigationButton(frame_buttons, text="Help",
                                            bootstyle="info",
                                      command=self.show_help)

    #####################
    # Getters & Setters #
    #####################

    def get_locality(self):
        return self.locality_entry.get()

    def set_locality(self, value):
        self.locality_entry.set(value)

    def get_formfeed(self):
        return self.formfeed_entry.get()

    def set_formfeed(self, value):
        self.formfeed_entry.delete(0, tk.END)
        self.formfeed_entry.insert(0, value)

    def get_diagram_chars(self):
        return self.diagram_entry.get()

    def set_diagram_chars(self, value):
        self.diagram_entry.delete(0, tk.END)
        self.diagram_entry.insert(0, value)

    def get_trimmed_ascii(self):
        return self.ascii_entry.get()

    def set_trimmed_ascii(self, value):
        self.ascii_entry.set(value)

    ###########
    # Methods #
    ###########

    def ok_pressed(self):
        self.locality[0] = self.get_locality()
        self.formfeed[0] = self.get_formfeed()
        self.diagram_chars[0] = self.get_diagram_chars()
        self.trimmed_ascii[0] = self.get_trimmed_ascii()
        self.exit()

    def show_help(self):
        # TODO: Implement help functionality
        pass

    def exit(self):
        self.destroy()
