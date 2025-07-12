from tkinter import filedialog, Menu
import ttkbootstrap as ttk
from typing import List
from lib.components.form import *
from lib.utils import *

MISSING_RANGES_NUM = 5

l_MISSING_VALUES = "What number-ranges are to be considerd as missing values?"

l_DECIMAL_PLACES = "How many decimal " \
                   "places are used " \
                   "in specifying " \
                   "each matrix entry (e.g coefficient) ? (0-9)"

l_FIELD_WIDTH = "What is the total field-width of each matrix cell? (1-10)"

l_ENTRIES_NUM_IN_ROW = "How many matrix " \
                       "entries are in " \
                       "each physical " \
                       "row? (2-98)"

l_VAR_NUM = "How many objects " \
            "(Variables) are " \
            "to be mapped? (" \
            "3-98)"

ENTRIES_PADX = 20

class MatrixInputPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.create_entries()
        # self.create_navigation()

    def reset_entries(self):
        pass

    def create_entries(self):
        # main frame
        frame_main = ttk.Frame(self)
        frame_main.pack(fill='both', expand=True)
        # Data File Frame
        frame_data_file = ttk.Frame(frame_main)
        frame_data_file.pack(fill='x', padx=ENTRIES_PADX, pady=(40, 0))
        # Data File Entry
        label_data_file = Label(frame_data_file, text="Matrix File:")
        label_data_file.pack(side=ttk.LEFT, padx=(0, 10))
        data_file_path = ttk.StringVar()
        self.entry_data_file = ttk.Entry(frame_data_file, width=65,
                                         validate="focusout",
                                         textvariable=data_file_path, )
        self.entry_data_file.pack(side=ttk.LEFT, fill='x', expand=False,
                                  padx=(25, 0))
        self.button_browse = ttk.Button(frame_data_file, text="Browse")
        self.button_browse.pack(side=ttk.RIGHT, padx=(0, 8))
        # Entries
        self.entry_var_num = self.label_entry(frame_main, l_VAR_NUM, 3)
        self.entry_entries_num_in_row = self.label_entry(frame_main,
                                                         l_ENTRIES_NUM_IN_ROW,
                                                         8)
        self.entry_field_width = self.label_entry(frame_main, l_FIELD_WIDTH,
                                                  10)
        self.entry_decimal_places = self.label_entry(frame_main,
                                                     l_DECIMAL_PLACES, 7)
        #
        frame_missing_values = ttk.Frame(frame_main)
        frame_missing_values.pack(fill='both', expand=True, pady=(24, 10))
        self.newline_label(frame_missing_values, l_MISSING_VALUES)
        self.from_entries = self.label_multi_entry(frame_missing_values,
                                              "From:", MISSING_RANGES_NUM,
                                              default=99.)
        self.to_entries = self.label_multi_entry(frame_missing_values,
                                            "To:", MISSING_RANGES_NUM,
                                            default=99.)

    ####################
    #    Validator     #
    ####################

    def validate_conversion(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except TypeError as e:
                if IS_PRODUCTION():
                    raise TypeError("Make sure all entries are valid integers "
                                     "or floats (for missing values).")
                else: raise e
        return wrapper


    #######################
    # Getters and Setters #
    #######################
    def get_data_file_path(self):
        return self.entry_data_file.get()

    def set_data_file_path(self, path):
        self.entry_data_file.delete(0, ttk.END)
        self.entry_data_file.insert(0, path)

    @validate_conversion
    def get_entries_num_in_row(self):
        return int(self.entry_entries_num_in_row.get())

    def set_entries_num_in_row(self, entries_num_in_row):
        self.entry_entries_num_in_row.delete(0, ttk.END)
        self.entry_entries_num_in_row.insert(0, entries_num_in_row)

    @validate_conversion
    def get_field_width(self):
        return int(self.entry_field_width.get())

    def set_field_width(self, field_width):
        self.entry_field_width.delete(0, ttk.END)
        self.entry_field_width.insert(0, field_width)

    @validate_conversion
    def get_decimal_places(self):
        return int(self.entry_decimal_places.get())

    def set_decimal_places(self, decimal_places):
        self.entry_decimal_places.delete(0, ttk.END)
        self.entry_decimal_places.insert(0, decimal_places)

    @validate_conversion
    def get_var_num(self):
        return int(self.entry_var_num.get())

    def set_var_num(self, var_num):
        self.entry_var_num.delete(0, ttk.END)
        self.entry_var_num.insert(0, var_num)

    @validate_conversion
    def get_missing_ranges(self):
        ranges = []
        for i in range(MISSING_RANGES_NUM):
            from_entry = self.from_entries[i].get().strip() or 0
            to_entry = self.to_entries[i].get().strip() or 0
            ranges.append((float(from_entry), float(to_entry)))
        return ranges

    def set_missing_ranges(self, missing_ranges: List[List[float]]):
        for i in range(MISSING_RANGES_NUM):
            self.from_entries[i].delete(0, ttk.END)
            self.from_entries[i].insert(0, str(missing_ranges[i][0]))
            self.to_entries[i].delete(0, ttk.END)
            self.to_entries[i].insert(0, str(missing_ranges[i][1]))

    def get_matrix_details(self) -> dict:
        return {
            "var_num": self.get_var_num(),
            "entries_num_in_row": self.get_entries_num_in_row(),
            "field_width": self.get_field_width(),
            "decimal_places": self.get_decimal_places(),
            "missing_ranges": self.get_missing_ranges()
        }

    ########################
    # Gui Helper Functions #
    ########################

    def newline_label(self, frame, text):
        missing_label_frame = ttk.Frame(frame)
        missing_label_frame.pack(fill='x')
        missing_label = Label(missing_label_frame, text=text)
        missing_label.pack(side="left", padx=ENTRIES_PADX)

    def label_entry(self, frame, label, default=None):
        var_num_frame = ttk.Frame(frame)
        var_num_frame.pack(fill='x', padx=ENTRIES_PADX, pady=(15, 0))
        label_var_num = Label(var_num_frame, text=label,
                                  wraplength=real_size(600), justify='left')
        label_var_num.pack(side=ttk.LEFT, padx=(0, 10))
        entry = ttk.Entry(var_num_frame, width=8)
        if default: entry.insert(0, default)
        entry.pack(side=ttk.RIGHT, padx=(25, 0))
        return entry

    def label_multi_entry(self, frame, label, n, default=None):
        var_num_frame = ttk.Frame(frame)
        var_num_frame.pack(fill='x', padx=(ENTRIES_PADX,70), pady=(15, 0))
        label_var_num = Label(var_num_frame, text=label,
                                  wraplength=real_size(600), justify='left')
        label_var_num.pack(side=ttk.LEFT, padx=(0, 5))
        entries = []
        for i in range(n):
            entry = ttk.Entry(var_num_frame, width=9)
            if default is not None:
                entry.insert(0, default)
            entry.pack(side=ttk.RIGHT, padx=(20, 0))
            entries.append(entry)
        return entries

    ####################
    # Event Functions #
    ####################

    def browse_file(self):
        # set the default extension to .txt, .MAT and .CSV
        filename = filedialog.askopenfilename(filetypes=[("Matrix files (.TXT, .MAT, .CSV)",
                                                           ["*.txt", "*.MAT", "*.csv"])])
        if filename:
            self.entry_data_file.delete(0, ttk.END)
            self.entry_data_file.insert(0, filename)

    def set_data_file_path(self, path):
        self.entry_data_file.delete(0, ttk.END)
        self.entry_data_file.insert(0, path)
