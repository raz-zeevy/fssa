from tkinter import filedialog, Menu
import ttkbootstrap as ttk

import lib.components.form
from lib.utils import *

ENTRIES_PADX = 20

class StartPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.create_entries()
        # self.create_navigation()

    def create_entries(self):
        # Data File Frame
        frame_data_file = ttk.Frame(self)
        frame_data_file.pack(fill='x', padx=ENTRIES_PADX, pady=(40, 0))
        # Data File Entry
        label_data_file = ttk.Label(frame_data_file, text="Data File:")
        label_data_file.pack(side=ttk.LEFT, padx=(0, 10))
        # def validate(x):
        #     if self.entry_data_file.get() : self.button_manual_input.state([
        #         '!disabled'])
        #     else: self.button_manual_input.state(['disabled'])
        data_file_path = ttk.StringVar()
        self.entry_data_file = ttk.Entry(frame_data_file, width=50,
                                         validate="focusout",
                                         textvariable=data_file_path,)
        self.entry_data_file.pack(side=ttk.LEFT, fill='x', expand=True)
        self.button_browse = ttk.Button(frame_data_file, text="Browse")
        self.button_browse.pack(side=ttk.LEFT, padx=10)
        # Lines per Case Frame
        frame_lines = ttk.Frame(self)
        frame_lines.pack(fill='x', padx=ENTRIES_PADX, pady=(30,10))
        # Records per Case Entry
        label_lines = ttk.Label(frame_lines,
                                  text="How many lines per case ? (1-99)")
        label_lines.pack(side=ttk.LEFT)
        self.entry_lines = ttk.Entry(frame_lines, width=5)
        self.entry_lines.pack(side=ttk.RIGHT, padx=ENTRIES_PADX)
        # Delimiter Frame
        frame_delimiter = ttk.Frame(self)
        frame_delimiter.pack(fill='x', padx=ENTRIES_PADX, pady=10)
        # What is the delimiter Entry
        label_delimiter = ttk.Label(frame_delimiter,
                                  text='Delimiter : (e.g. tab, comma, space)')
        label_delimiter.pack(side=ttk.LEFT)
        self.entry_delimiter = ttk.Entry(frame_delimiter, width=5)
        self.entry_delimiter.pack(side=ttk.RIGHT, padx=ENTRIES_PADX)
        # Fixed Width
        frame_fixed_width = ttk.Frame(self)
        frame_fixed_width.pack(fill='x', padx=ENTRIES_PADX, pady=10)
        # Label for the text
        label_text = ttk.Label(frame_fixed_width,
                                 text="Is the data file in fixed width "
                                      f"format ? ({DELIMITER_1_D}, {DELIMITER_2_D})",
                                    anchor='w',  # Aligns text to the west (left)
                                    justify=ttk.LEFT,
                                    wraplength=WINDOW_WIDTH - 50)
        label_text.pack(side=ttk.LEFT, fill='x', expand=True)
        self.selection_box_fixed_width = lib.components.form.SelectionBox(
            frame_fixed_width,
            default="No",
            width=5,
            values=["No",DELIMITER_1_D, DELIMITER_2_D])
        self.selection_box_fixed_width.pack(side=ttk.RIGHT, padx=ENTRIES_PADX)
        # Manual Input
        frame_manual_input = ttk.Frame(self)
        frame_manual_input.pack(fill='x', padx=ENTRIES_PADX, pady=10)
        # Label for the text
        label_text = ttk.Label(frame_manual_input,
                                 text="Do you want to manually parse the "
                                      "input data file variables ?",
                                    anchor='w',  # Aligns text to the west (left)
                                    justify=ttk.LEFT,
                                    wraplength=WINDOW_WIDTH - 50)
        label_text.pack(side=ttk.LEFT, fill='x', expand=True)
        self.manual_input_var = ttk.BooleanVar(value=False)
        self.check_box_manual_input = ttk.Checkbutton(frame_manual_input,
                                                 bootstyle="round-toggle",
                                                 variable=self.manual_input_var,
                                                 onvalue=True,
                                                 offvalue=False,)
        self.check_box_manual_input.pack(side=ttk.RIGHT, padx=(0,27))
        # Missing Value Frame
        frame_missing_value = ttk.Frame(self)
        frame_missing_value.pack(fill='x', padx=ENTRIES_PADX, pady=10)
        # Label for the text
        label_text = ttk.Label(frame_missing_value,
                               text="Is zero (0) a valid value or are "
                                    "values "
                                    "other then zero (0) represent missing "
                                    "values?",
                               anchor='w',  # Aligns text to the west (left)
                               justify=ttk.LEFT,
                               wraplength=WINDOW_WIDTH - 200)
        label_text.pack(side=ttk.LEFT, fill='x', expand=True)
        # Checkbox, without text, aligned to the right
        self.missing_value_var = ttk.BooleanVar(value=False)
        self.checkbox_missing_value = ttk.Checkbutton(frame_missing_value,
                                                 bootstyle="round-toggle",
                                                 variable=self.missing_value_var,
                                                 command =
                                                 self.on_missing_value_change,
                                                 onvalue=True,
                                                 offvalue=False)
        self.checkbox_missing_value.pack(side=ttk.RIGHT, padx=(0,27))

    def set_delimiter(self, delimiter, readonly=True):
        self.entry_delimiter.state(['!readonly'])
        self.entry_delimiter.delete(0, ttk.END)
        self.entry_delimiter.insert(0, delimiter)
        #
        self.entry_lines.state(['!readonly'])
        self.selection_box_fixed_width.state(['!disabled'])
        if delimiter == DELIMITER_1_D:
            self.selection_box_fixed_width.set(DELIMITER_1_D)
            self.entry_delimiter.delete(0, ttk.END)
        if readonly:
            self.entry_delimiter.state(['readonly'])
            self.entry_lines.state(['readonly'])
            self.selection_box_fixed_width.set("No")
            self.selection_box_fixed_width.state(['disabled'])

    def on_manual_input_change(self):
        if self.manual_input_var.get():
            self.entry_delimiter.state(['readonly'])
            self.entry_delimiter.delete(0, ttk.END)
            self.selection_box_fixed_width.state(['disabled'])
            self.selection_box_fixed_width.set("No")
        else:
            self.entry_delimiter.state(['!readonly'])
            self.selection_box_fixed_width.state(['!disabled'])
            self.selection_box_fixed_width.set("No")
    def on_missing_value_change(self):
        if self.missing_value_var.get():
            if not self.manual_input_var.get():
                self.check_box_manual_input.invoke()
            self.check_box_manual_input.state(['disabled'])
        else:
            self.check_box_manual_input.state(['!disabled'])


    def browse_file(self):
        filename = filedialog.askopenfilename()
        self.entry_data_file.delete(0, ttk.END)
        self.entry_data_file.insert(0, filename)

    def set_entry_lines(self, lines : int):
        self.entry_lines.delete(0, ttk.END)
        self.entry_lines.insert(0, f"{lines}")

    def set_data_file_path(self, path):
        self.entry_data_file.delete(0, ttk.END)
        self.entry_data_file.insert(0, path)

    def get_delimiter(self):
        def check_string(string, value):
            if string in [value, value.upper(), value.lower()]:
                return True
        delimiter = self.entry_delimiter.get()
        if delimiter != "" and \
                self.selection_box_fixed_width.get() != "No":
            raise ValueError("You can't have both a delimiter and a fixed width")
        if check_string(delimiter, "space"):
            return " "
        elif check_string(delimiter, "tab"):
            return "\t"
        elif check_string(delimiter, "comma"):
            return ","
        return self.entry_delimiter.get() or self.selection_box_fixed_width.get()

    def default_entry_lines(self):
        self.set_entry_lines(1)

    def get_data_file_path(self):
        return self.entry_data_file.get()

    def get_lines_per_var(self):
        if self.entry_lines.get():
            return int(self.entry_lines.get())
        return 0