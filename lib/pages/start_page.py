from tkinter import filedialog, Menu
import ttkbootstrap as ttk
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
                                         validatecommand=self.on_data_file_path_change,
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
        # Lines per Case Frame
        frame_delimiter = ttk.Frame(self)
        frame_delimiter.pack(fill='x', padx=ENTRIES_PADX, pady=10)
        # What is the delimiter Entry
        label_delimiter = ttk.Label(frame_delimiter,
                                  text="Delimiter (e.g. comma, tab, space, "
                                       "1d, 2d):")
        label_delimiter.pack(side=ttk.LEFT)
        self.entry_delimiter = ttk.Entry(frame_delimiter, width=5)
        self.entry_delimiter.pack(side=ttk.RIGHT, padx=ENTRIES_PADX)
        # Manual Input
        frame_manual_input = ttk.Frame(self)
        frame_manual_input.pack(fill='x', padx=ENTRIES_PADX, pady=10)
        # Label for the text
        label_text = ttk.Label(frame_manual_input,
                                 text="Do you want to manually parse the "
                                      "input data file ?",
                                    anchor='w',  # Aligns text to the west (left)
                                    justify=ttk.LEFT,
                                    wraplength=WINDOW_WIDTH - 50)
        label_text.pack(side=ttk.LEFT, fill='x', expand=True)
        # Button texted "Manual Input", aligned to the right
        self.button_manual_input = ttk.Button(frame_manual_input,
                                         text="Manual Input..",)
        self.button_manual_input.pack(side=ttk.RIGHT)
        self.button_manual_input.config(state='disabled')
        # self.button_manual_input.update()
        # Missing Value Frame
        frame_missing_value = ttk.Frame(self)
        frame_missing_value.pack(fill='x', padx=ENTRIES_PADX, pady=10)
        # Label for the text
        label_text = ttk.Label(frame_missing_value,
                               text="Is zero (0) the missing value, and the ONLY missing value, for ALL variables that are going to be processed in this run ?",
                               anchor='w',  # Aligns text to the west (left)
                               justify=ttk.LEFT,
                               wraplength=WINDOW_WIDTH - 50)
        label_text.pack(side=ttk.LEFT, fill='x', expand=True)
        # Checkbox, without text, aligned to the right
        self.missing_value_var = ttk.BooleanVar(value=True)
        checkbox_missing_value = ttk.Checkbutton(frame_missing_value,
                                                 variable=self.missing_value_var,
                                                 onvalue=True,
                                                 offvalue=False)
        checkbox_missing_value.pack(side=ttk.RIGHT, padx=5)
        data_file_path.trace('w', self.on_data_file_path_change())

    def on_data_file_path_change(self):
        if self.entry_data_file.get() :
            self.button_manual_input.state(['!disabled'])
        else: self.button_manual_input.state(['disabled'])

    def set_delimiter(self, delimiter, readonly=True):
        self.entry_delimiter.state(['!readonly'])
        self.entry_lines.state(['!readonly'])
        self.entry_delimiter.delete(0, ttk.END)
        self.entry_delimiter.insert(0, delimiter)
        if readonly:
            self.entry_delimiter.state(['readonly'])
            self.entry_lines.state(['readonly'])

    def save_file(self):
        file_name = filedialog.asksaveasfilename(filetypes=[('csv', '*.csv')],
                                                 defaultextension=".csv")
        return file_name
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
    def default_entry_lines(self):
        self.set_entry_lines(1)

    def get_data_file_path(self):
        return self.entry_data_file.get()

    def get_lines_per_var(self):
        if self.entry_lines.get():
            return int(self.entry_lines.get())
        return 0