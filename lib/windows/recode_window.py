import os
import ttkbootstrap as ttk
import tkinter as tk
from lib.moduls.help_content import *
from lib.components.window import Window
from lib.utils import *
from lib.components.form import *



class RecodeWindow(Window):
    def __init__(self, parent,**kwargs):
        """
        """
        super().__init__(**kwargs, geometry="600x450")
        self.title("Recode Variables")
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
        # add for a string of the indices of the variables to recode
        indices_frame = ttk.Frame(self)
        indices_frame.pack(side=tk.TOP, fill='x', padx=10, pady=(20,0))
        self.indices_label = ttk.Label(indices_frame,
                                       text="Enter the serial number of "
                                            "the variables you wish to "
                                            "recode: (e.g. 1-5, 8, 11-13)",
                                       justify="left", wraplength=real_size(
                300))
        self.indices_label.pack(side=tk.LEFT, padx=5)
        self.indices_entry = ttk.Entry(indices_frame, width=20)
        self.indices_entry.pack(side=tk.RIGHT, padx=(0,20), pady=(10,0))
        grouping_frame = ttk.Frame(self)
        grouping_frame.pack(side=tk.TOP, fill='x', padx=10, pady=(20,0))
        self.grouping_label = ttk.Label(grouping_frame,
                                        text="Would you like to recode the "
                                             "data into groups? If yes, "
                                             "to how many groups?",
                                        wraplength=real_size(400),
                                        justify="left")
        self.grouping_label.pack(side=tk.LEFT, padx=5, fill="x")
        grouping_values = [str(i) for i in range(1,100)]
        grouping_values.insert(0, "No")
        self.grouping_entry = SelectionBox(grouping_frame,
                                           values=grouping_values,
                                           width=5,)
        self.grouping_entry.bind("<<ComboboxSelected>>", lambda x:
                                 self.on_grouping_change())

        self.grouping_entry.pack(side=tk.RIGHT, padx=(0,20), pady=(10,0))
        # Grouping Type
        grouping_type_frame = ttk.Frame(self)
        grouping_type_frame.pack(side=tk.TOP, fill='x', padx=10, pady=(20,0))
        self.grouping_type_label = ttk.Label(grouping_type_frame,
                                                text="How would you like to "
                                                     "group the data?",
                                                wraplength=real_size(400),
                                             justify="left")
        self.grouping_type_label.pack(side=tk.LEFT, padx=5, fill="x")

        self.grouping_type_entry = SelectionBox(grouping_type_frame,
                                                values=GROUPING_TYPES,
                                                width=10)
        self.grouping_type_entry.pack(side=tk.RIGHT, padx=(0,20), pady=(10,0))
        # Inverting
        inverting_frame = ttk.Frame(self)
        inverting_frame.pack(side=tk.TOP, fill='x', padx=10, pady=(20,0))
        self.inverting_label = ttk.Label(inverting_frame,
                                        text="Would you like to invert the "
                                             "values of the variable?\n(e.g. "
                                             "[1,"
                                             "2,3] → [3,2,1] )",
                                        wraplength=real_size(400),
                                         justify="left")
        self.inverting_label.pack(side=tk.LEFT, padx=5, fill="x")
        self.inverting_var = ttk.BooleanVar(value=False)
        self.inverting_check_box = ttk.Checkbutton(inverting_frame,
                                                 bootstyle="round-toggle",
                                                 variable=self.inverting_var,
                                                 onvalue=True,
                                                 offvalue=False,
                                                   command=self.on_inverting_change)
        self.inverting_check_box.pack(side=ttk.RIGHT, padx=(0,27))

        # default values
        self.grouping_entry.current(9)
        self.grouping_type_entry.current(0)

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
        self.button_recode = NavigationButton(frame_buttons, text="Recode",
                                        command=self.recode,)
        self.button_recode.pack(side=tk.LEFT, padx=30)

    #####################
    # Getters & Setters #
    #####################

    def set_indices(self, indices_string : str):
        self.indices_entry.delete(0, tk.END)
        self.indices_entry.insert(0, indices_string)

    def set_grouping(self, groups_num):
        self.grouping_entry.current(groups_num)

    def set_grouping_type(self, grouping_type : str):
        if grouping_type not in GROUPING_TYPES:
            raise ValueError("Invalid grouping type")
        self.grouping_type_entry.set(grouping_type)

    def set_inverting(self, state: bool):
        if self.inverting_var.get() == state:
            pass
        else:
            self.inverting_check_box.invoke()

    def get_indices(self):
        return self.indices_entry.get()

    def get_grouping(self):
        if self.grouping_entry.get() == "No":
            return 0
        return self.grouping_entry.get()

    def get_grouping_type(self):
        return self.grouping_type_entry.get()

    def get_inverting(self):
        return self.inverting_var.get()

    def get_recoding_details(self):
        return {
            "indices_string": self.get_indices(),
            "grouping": int(self.get_grouping()),
            "grouping_type": self.get_grouping_type(),  # "Percentile" or "Equal Range
            "inverting": self.get_inverting()
        }

    ###########
    # Methods #
    ###########

    def on_grouping_change(self):
        if self.grouping_entry.get() == "No":
            self.grouping_type_entry.state(['disabled'])
            self.grouping_type_entry.current(0)
        else:
            self.grouping_type_entry.state(['!disabled'])

    def on_inverting_change(self):
        if self.inverting_var.get():
            self.grouping_type_entry.state(['disabled'])
            self.grouping_entry.current(0)
            self.grouping_entry.state(['disabled'])
        else:
            self.grouping_entry.state(['!disabled'])
            if self.grouping_entry.get() != "No":
                self.grouping_type_entry.state(['!disabled'])

    def recode(self):
        pass

    def exit(self):
        self.destroy()
