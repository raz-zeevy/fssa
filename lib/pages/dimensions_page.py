from tkinter import filedialog, Menu
import ttkbootstrap as ttk
from lib.utils import *
from lib.components.form import *


ENTRIES_PADX = 20
DIMENSION_OPTIONS = [
    "Single Dimensionality",
    "Dimensions Range",
]
class DimensionsPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.frame_dimensions_band = None
        self.dimension_boxes = None
        self.create_entries()


    def set_number_of_variables(self, num):
        self.label_var_num.config(text=f"You have selected {num} "
                                           f"variables")

    def create_entries(self):
        frame_var_label = ttk.Frame(self)
        frame_var_label.pack(fill='x', padx=ENTRIES_PADX, pady=(20, 0))
        self.label_var_num = Label(frame_var_label,text="")
        self.label_var_num.pack(side=ttk.LEFT)
        ####
        frame_correlation_combo = ttk.Frame(self)
        frame_correlation_combo.pack(fill='x', padx=ENTRIES_PADX, pady=(20, 0))
        #
        self.correlation_label = Label(frame_correlation_combo,
                                      text="Type of coefficients to "
                                           "generate and use: ",
                                      )
        self.correlation_label.pack(side=ttk.LEFT)
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
        dimension_label = Label(frame_dimension_combo,
                                    text="Dimensionality: ",
                                    )
        dimension_label.pack(side=ttk.LEFT)
        #
        self.dimension_combo = ttk.Combobox(frame_dimension_combo,
                                            state="readonly",
                                       values=DIMENSION_OPTIONS,)
        self.dimension_combo.pack(side=ttk.RIGHT)
        self.dimension_combo.bind("<<ComboboxSelected>>",
                                  self.dimension_combo_selected)
        ###
        self.frame_dimensions_band = ttk.Frame(self)
        self.frame_dimensions_band.pack(fill='x', padx=ENTRIES_PADX,
                                        pady=(0, 0))
        ###
        self.dimension_combo.current(0)
        self.dimension_combo_selected(None)

    def dimension_combo_selected(self, event):
        for widget in self.frame_dimensions_band.winfo_children():
            widget.destroy()
        if self.dimension_combo.get() == DIMENSION_OPTIONS[0]:
            self.dimension_boxes = [self.create_dim_selection_box(
                self.frame_dimensions_band,
                                  "Dimension:")]
        else:
            self.dimension_boxes = [
                self.create_dim_selection_box(
                    self.frame_dimensions_band, "Lowest Dimensionality:"),
                self.create_dim_selection_box(
                    self.frame_dimensions_band, "Highest Dimensionality:")
            ]
            # set the default to 3
            self.dimension_boxes[-1].current(1)
            self.dimension_boxes[-1].bind("<<ComboboxSelected>>",
                                          self.on_dim_range_selected)
            self.dimension_boxes[0].bind("<<ComboboxSelected>>",
                                          self.on_dim_range_selected)

    def on_dim_range_selected(self, event):
        high = self.dimension_boxes[-1]
        low = self.dimension_boxes[0]
        if int(high.get()) < int(low.get()):
            high.set(low.get())

    def get_dimensions(self):
        return [int(box.get()) for box in self.dimension_boxes]

    def set_dims(self, min, max=None):
        if max and len(self.dimension_boxes) == 1:
            self.dimension_combo.set(DIMENSION_OPTIONS[1])
            self.dimension_combo_selected(None)
        self.dimension_boxes[0].set(min)
        if max:
            self.dimension_boxes[1].set(max)
    def get_correlation_type(self):
        return self.correlation_combo.get()

    def set_correlation_type(self, type):
        self.correlation_combo.set(type)

    def create_dim_selection_box(self, master, text):
        """Create and pack an equalizer band"""
        frame_band = ttk.Frame(master)
        frame_band.pack(fill='x',pady=(20,0))
        # # header label
        hdr = Label(frame_band, text=text)
        hdr.pack(side=ttk.LEFT, fill='x', pady=5, padx=(0,40))
        # value label
        box = SelectionBox(frame_band,
                            width=4,
            values=[str(i) for i in range(2,9)],
                           default='2'
        )
        box.pack(side=ttk.RIGHT)
        return box

    def set_matrix_mode(self):
        self.correlation_combo.set(SIMILARITY)
        self.correlation_combo.config(values=[SIMILARITY, DISSIMILARITY])
        self.correlation_label.config(text="Coefficients in matrix designate:")

    def set_default(self):
        self.dimension_combo.current(0)
        self.dimension_combo_selected(None)
        self.correlation_combo.current(0)