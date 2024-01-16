from tkinter import filedialog, Menu
import ttkbootstrap as ttk
from lib.utils import *

ENTRIES_PADX = 20

class StartPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.create_entries()
        self.create_navigation()

    def create_entries(self):
        # Data File Frame
        frame_data_file = ttk.Frame(self)
        frame_data_file.pack(fill='x', padx=ENTRIES_PADX, pady=(40, 0))
        # Data File Entry
        label_data_file = ttk.Label(frame_data_file, text="Data File:")
        label_data_file.pack(side=ttk.LEFT, padx=(0, 10))
        self.entry_data_file = ttk.Entry(frame_data_file, width=50)
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

    def create_navigation(self):
        # Navigation Buttons Frame
        frame_navigation = ttk.Frame(self)
        # pack the navigation at the bottom of the screen but above the help
        # bar
        frame_navigation.pack(side=ttk.BOTTOM, fill='x', padx=10,
                              pady=5)
        center_frame = ttk.Frame(frame_navigation)
        center_frame.pack(pady=5, expand=True)
        self.button_next = ttk.Button(center_frame, text="Next")
        self.button_next.pack(side=ttk.LEFT, padx=5)

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
        self.entry_lines.delete(0, ttk.END)
        self.entry_lines.insert(0, "1")