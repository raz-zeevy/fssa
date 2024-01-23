from tkinter import filedialog, Menu
import ttkbootstrap as ttk
from lib.utils import *
import tkinter as tk
from ttkbootstrap import Canvas, Frame, Scrollbar, Label

# Constants for the layout
TABLE_PADX = 20
ENTRIES_PADX = 40
WIDTH_FACET_COMBO = 10

class FacetVarPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.combo_by_var = []
        self.main_table_frame = None
        self.parent = parent
        self.create_entries()
        self.width_facet_combo = WIDTH_FACET_COMBO
    def create_entries(self):
        frame_correlation_combo = ttk.Frame(self)
        frame_correlation_combo.pack(fill='x', padx=ENTRIES_PADX, pady=(20,
                                                                        20))

        correlation_label = ttk.Label(frame_correlation_combo,
                                      text="For each variable below, specifu "
                                           "its facet element in each facet")
        correlation_label.pack(side="left")

    def create_facet_variable_table(self, var_labels, facet_details):
        """
        Create the table layout for the facet variables page
        :param var_labels: eg. ["first", "", "third_label]
        :param facet_details:  [[a,b,c], [a,b,c,d,e], [a,b]]
        :return:
        """
        var_num = len(var_labels)
        num_facets = len(facet_details)

        def on_frame_configure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_mousewheel(event, canvas):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        if self.main_table_frame:
            for widget in self.main_table_frame.winfo_children():
                widget.destroy()
            self.combo_by_var = []

        # Create a frame for the table and self.scrollbar
        self.main_table_frame = Frame(self)
        self.main_table_frame.pack(fill='both', expand=True, padx=TABLE_PADX,
                               pady=(0, 20))

        # Create a frame for the header
        self.header_frame = Frame(self.main_table_frame)
        self.header_frame.pack(fill='x', padx=(TABLE_PADX,75))

        # Create headers
        headers = ["Variable"] + [f"Facet {chr(65 + i)}" for i in range(
            num_facets)]
        # Define a dictionary to keep track of the width of each column based on the header
        column_widths = {}
        header_widgets = []
        header_colspan = (1, 3, 3, 3, 3)
        for col, text in enumerate(headers):
            header_label = Label(self.header_frame, text=text, borderwidth=1,
                                 relief="solid", bootstyle='primary-inverse')
            header_label.grid(row=0, column=col,
                              columnspan=header_colspan[col],sticky='ew')
            header_widgets.append(header_label)

        # Create a frame for the canvas and self.scrollbar
        table_container = Frame(self.main_table_frame)
        table_container.pack(fill='both', expand=True, padx=TABLE_PADX, pady=0)

        # Create canvas and self.scrollbar
        combo_canvas = Canvas(table_container)
        combo_canvas.pack(side='left', fill='both', expand=True)

        self.scrollbar = Scrollbar(table_container, command=combo_canvas.yview)
        self.scrollbar.pack(side='right', fill='y')

        combo_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame within the canvas to hold the table contents
        self.table_frame = Frame(combo_canvas)
        self.table_frame.pack(fill='both', expand=True)
        self.table_frame.bind("<Configure>", lambda event: on_frame_configure(
            combo_canvas))
        combo_canvas.create_window((0, 0),
                                   window=self.table_frame,
                                   anchor='nw')
        # Bind the mousewheel event to the self.scrollbar
        combo_canvas.bind_all("<MouseWheel>",
                              lambda event: on_mousewheel(event, combo_canvas))

        # Table of comboboxes
        for row in range(1, var_num + 1):
            var_label = var_labels[row - 1]
            var_combos = []
            if var_label == "":
                var_label = f"Variable {row:02d}"
            else:
                var_label = f"{row:02d} {var_label}"+ " "*(12-len(var_label))
            Label(self.table_frame, text=var_label,
                  borderwidth=0.5, relief="solid",
                  bootstyle='primary').grid(row=row - 1, column=0, sticky='ew', ipady=7)
            for col in range(1, num_facets + 1):
                values = ["Undefined"] + facet_details[col - 1]
                combobox = ttk.Combobox(self.table_frame,
                                        values=values,
                                        width=self.width_facet_combo,
                                        state="readonly")
                var_combos.append(combobox)
                combobox.grid(row=row - 1, column=col, sticky='ew', padx=1, pady=1, ipady=0)
                combobox.set(values[0])  # Set the first option
                combobox.unbind_class("TCombobox", "<MouseWheel>")
            self.combo_by_var.append(var_combos)
        # Adjust column configuration for equal width
        col_weights = (1,16,16,16,16)
        self.table_frame.grid_columnconfigure(0, weight=1)
        for col in range(num_facets + 1):
            self.header_frame.grid_columnconfigure(col, weight=col_weights[
                col])
            self.table_frame.grid_columnconfigure(col, weight=3)

    def get_all_var_facets_indices(self):
        data = []
        for i, var in enumerate(self.combo_by_var):
            var_facets = []
            for j, facet_index in enumerate(var):
                var_facets.append(facet_index.current())
            data.append(var_facets)
        return data