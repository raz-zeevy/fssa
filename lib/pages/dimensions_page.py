from tkinter import filedialog, Menu
import ttkbootstrap as ttk
from lib.utils import *

ENTRIES_PADX = 20

class DimensionsPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.frame_dimensions_band = None
        self.dimension_scales = None
        self.create_entries()

    def create_entries(self):
        frame_var_label = ttk.Frame(self)
        frame_var_label.pack(fill='x', padx=ENTRIES_PADX, pady=(20, 0))
        label_var_num = ttk.Label(frame_var_label,
            text="You have selected 5 Variables")
        label_var_num.pack(side=ttk.LEFT)
        ####
        frame_correlation_combo = ttk.Frame(self)
        frame_correlation_combo.pack(fill='x', padx=ENTRIES_PADX, pady=(20, 0))
        #
        correlation_label = ttk.Label(frame_correlation_combo,
                                      text="Type of coefficients to "
                                           "generate and use: ",
                                      )
        correlation_label.pack(side=ttk.LEFT)
        #
        self.correlation_combo = ttk.Combobox(frame_correlation_combo,
                                              state="readonly",
                                              values=[MONO,
                                                      PEARSON], )
        self.correlation_combo.pack(side=ttk.RIGHT)
        self.correlation_combo.bind("<<ComboboxSelected>>",
                                    self.dimension_combo_selected)
        self.correlation_combo.current(0)
        # create a combobox between single dimension or dimension range
        frame_dimension_combo = ttk.Frame(self)
        frame_dimension_combo.pack(fill='x', padx=ENTRIES_PADX, pady=(20, 0))
        #
        dimension_label = ttk.Label(frame_dimension_combo,
                                    text="Dimensionality: ",
                                    )
        dimension_label.pack(side=ttk.LEFT)
        #
        self.dimension_combo = ttk.Combobox(frame_dimension_combo,
                                            state="readonly",
                                       values=["Single Dimension",
                                               "Dimensions Range"],)
        self.dimension_combo.pack(side=ttk.RIGHT)
        self.dimension_combo.bind("<<ComboboxSelected>>",
                                  self.dimension_combo_selected)
        ###
        self.frame_dimensions_band = ttk.Frame(self)
        self.frame_dimensions_band.pack(fill='x', padx=ENTRIES_PADX,
                                        pady=(20, 0))
        ###
        self.dimension_combo.current(0)
        self.dimension_combo_selected(None)

    def dimension_combo_selected(self, event):
        for widget in self.frame_dimensions_band.winfo_children():
            widget.destroy()
        if self.dimension_combo.get() == 'Single Dimension':
            self.dimension_scales = [self.create_band(
                self.frame_dimensions_band,
                                  "Dimension:")]
        else:
            self.dimension_scales = [
                self.create_band(
                    self.frame_dimensions_band, "Lowest Dimensionality:"),
                self.create_band(
                    self.frame_dimensions_band, "Highest Dimensionality:")
            ]

    def get_dimensions(self):
        return [int(scale.get()) for scale in self.dimension_scales]

    def set_dims(self, min, max=None):
        self.dimension_scales[0].set(min)
        if max:
            self.dimension_scales[1].set(max)
    def get_correlation_type(self):
        return self.correlation_combo.get()

    def create_band(self, master, text):
        """Create and pack an equalizer band"""
        value = 2
        # set the text_variable
        self.setvar(text, 2)

        frame_band = ttk.Frame(master)
        frame_band.pack(fill='x',pady=(20,0))
        # # header label
        hdr = ttk.Label(frame_band, text=text)
        hdr.pack(side=ttk.LEFT, fill='x', pady=5, padx=(0,40))
        # value label
        val = ttk.Label(master=frame_band, textvariable=text)
        val.pack(side=ttk.RIGHT, pady=0, padx=(0,25))
        scale = ttk.Scale(
            master=frame_band,
            orient="horizontal",
            from_=2,
            to=8,
            length=400,
            value=value,
            command=lambda x=value, y=text: self.update_value(x, y),
        )
        scale.pack(side=ttk.RIGHT, padx=(0,40))
        return scale

    def update_value(self, value, name):
        self.setvar(name, f"{float(value):.0f}")

    def update_value(self, value, name):
        self.setvar(name, f"{float(value):.0f}")

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