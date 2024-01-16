from tkinter import filedialog, Menu
import ttkbootstrap as ttk
from lib.utils import *

ENTRIES_PADX = 20

class FacetPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.create_entries()
        self.create_navigation()

    def create_entries(self):
        ####
        frame_correlation_combo = ttk.Frame(self)
        frame_correlation_combo.pack(fill='x', padx=ENTRIES_PADX, pady=(20, 0))
        #
        correlation_label = ttk.Label(frame_correlation_combo,
                                      text="How many facets (if any) do you "
                                           "want to define ?",
                                      )
        correlation_label.pack(side=ttk.LEFT)
        #
        self.correlation_combo = ttk.Combobox(frame_correlation_combo,
                                              state="readonly",
                                              values=["No facets",
                                                      "1 Facet",
                                                      "2 Facets",
                                                      "3 Facets",
                                                      "4 Facets"], )
        self.correlation_combo.pack(side=ttk.RIGHT)
        self.correlation_combo.current(0)

    def create_navigation(self):
        # Navigation Buttons Frame
        frame_navigation = ttk.Frame(self)
        # pack the navigation at the bottom of the screen but above the help
        # bar
        frame_navigation.pack(side=ttk.BOTTOM, fill='x', padx=10,
                              pady=5)
        center_frame = ttk.Frame(frame_navigation)
        center_frame.pack(pady=5, expand=True)
        self.button_previous = ttk.Button(center_frame,
                                          text="Previous")
        self.button_previous.pack(side=ttk.LEFT, padx=5)
        self.button_next = ttk.Button(center_frame,
                                          text="Next",
                                          state=ttk.DISABLED)
        self.button_next.pack(side=ttk.LEFT, padx=5)
        self.button_run = ttk.Button(center_frame, text="Run")
        self.button_run.pack(side=ttk.LEFT, padx=5)

    def set_delimiter(self, delimiter, readonly=True):
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