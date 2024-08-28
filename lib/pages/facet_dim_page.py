from tkinter import filedialog, Menu
import ttkbootstrap as ttk
from lib.utils import *
import tkinter as tk
from ttkbootstrap import Canvas, Frame, Scrollbar
from lib.components.form import *

# Constants for the layout
TABLE_PADX = 20
ENTRIES_PADX = 40
WIDTH_FACET_COMBO = 10


class FacetDimPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.parent = parent
        self.create_entries()
        self.facets_dim_check_buttons = {}
        self.main_frame = Frame(self)
        self.main_frame.pack(fill='both', expand=True, padx=TABLE_PADX,
                        pady=(0, 20))
    def create_entries(self):
        frame_correlation_combo = ttk.Frame(self)
        frame_correlation_combo.pack(fill='x', padx=ENTRIES_PADX, pady=(20,
                                                                        20))

        correlation_label = Label(frame_correlation_combo,
                                      text="Mark the dimensionalities for "
                                           "which facet diagrams will be "
                                           "created")
        correlation_label.pack(side="left")

    def create_facet_dimension_table(self, num_facets, max_dim, min_dim):
        if self.facets_dim_check_buttons:
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            self.facets_dim_check_buttons = {}
        self.validate_input(num_facets, max_dim, min_dim)
        # Create a frame for the canvas and self.scrollbar
        self.table_frame = Frame(self.main_frame)
        self.table_frame.pack(fill='both', expand=True, padx=TABLE_PADX,
                              pady=0)
        # Create headers
        headers = ["Dimension"] + [f"Facet {chr(65 + i)}" for i in range(
            num_facets)]
        for col, text in enumerate(headers):
            header_label = Label(self.table_frame, text=text, borderwidth=1,
                                 anchor='center',
                                 relief="solid",
                                 bootstyle='primary-inverse')
            header_label.grid(row=0, column=col, sticky='ew')
        # Table of check buttons
        for dim in range(min_dim, max_dim+1):
            dim_buttons = []
            dim_facet_label = ttk.Checkbutton(self.table_frame, text=dim,
                                              bootstyle="toolbutton", )
            dim_facet_label.state(['selected'])
            dim_facet_label.bind("<Button-1>", lambda e: None)
            dim_facet_label.grid(row=1 + dim, column=0,
                                 sticky='ew',
                                 padx=1, pady=1, ipady=0)
            for col in range(num_facets):
                check_var = tk.IntVar(value=1)
                dim_facet_button = ttk.Checkbutton(self.table_frame,
                                                   variable=check_var,
                                                   text="Yes",
                                                   onvalue=0,
                                                   offvalue=1,
                                                   bootstyle="secondary-outline-toolbutton")
                dim_facet_button.configure(command=lambda
                    var=check_var,
                    btn=dim_facet_button: self._update_checkbutton_text(var,
                                                                        btn))
                dim_buttons.append(dim_facet_button)
                dim_facet_button.grid(row=1 + dim, column=col + 1,
                                      sticky='ew',
                                      padx=1, pady=1, ipady=0
                                      )
                # by default
            self.facets_dim_check_buttons[dim] = (dim_buttons)
        # Adjust column configuration for equal width
        col_weights = [1] + [10] * num_facets
        self.table_frame.grid_columnconfigure(0, weight=1)
        for col in range(num_facets + 1):
            self.table_frame.grid_columnconfigure(col, weight=col_weights[col])

    def _update_checkbutton_text(self, var, btn):
        btn.config(text="Yes" if var.get() else "No")

    def get_facets_dim(self) -> dict:
        facet_dim = {}
        for dim, facets in self.facets_dim_check_buttons.items():
            facet_dim[dim] = [facet+1 for facet, btn in
                              enumerate(facets) if btn.cget("text") == "Yes"]
        return facet_dim

    def set_facets_dim(self, facet_dim_details):
        """
        :param facet_dim_details: eg. {2: [1, 2], 3: [1, 2, 3]}
        :return:
        """
        for dim, facets in self.facets_dim_check_buttons.items():
            for i, btn in enumerate(facets):
                if i + 1 not in facet_dim_details[str(dim)]:
                    btn.invoke()

    def validate_input(self, num_facets, max_dim, min_dim):
        if num_facets > 4:
            raise ValueError("The number of facets cannot exceed 4")
        if max_dim > 9:
            raise ValueError("The number of dimensions cannot exceed 9")
        if num_facets < 1:
            raise ValueError("The number of facets cannot be less than 1")
        if min_dim < 2:
            raise ValueError("The number of dimensions cannot be less than 2")
