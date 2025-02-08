from tkinter import filedialog, Menu
from typing import List
from lib.components.form import *
import ttkbootstrap as ttk
from lib.utils import *

MAX_FACET_NUM = 9
MIN_FACET_NUM = 2
ENTRIES_PADX = 20


class FacetPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.parent = parent
        self.colors = parent.root.style.colors
        self.width_facet_element_label_entry = round(WINDOW_WIDTH * 0.015)
        self.width_facet_combo = round(WINDOW_WIDTH * 0.015 / 3)
        self.facet_frames = []
        self.width = WINDOW_WIDTH
        self.facets_entries = []
        self.facets_elements_combo = []
        self.create_entries()
        # self.create_facet_container()

    def create_entries(self):
        """
        create entries for facet page
        :return:
        """
        frame_correlation_combo = ttk.Frame(self)
        frame_correlation_combo.pack(fill='x', padx=ENTRIES_PADX, pady=(20, 0))

        facet_label = Label(frame_correlation_combo,
                                text="How many facets (if any) do you want to define ?")
        facet_label.pack(side=ttk.LEFT)

        self.facets_combo = ttk.Combobox(frame_correlation_combo,
                                         state="readonly",
                                         values=["No facets", "1 Facet",
                                                 "2 Facets", "3 Facets",
                                                 "4 Facets"])
        self.facets_combo.pack(side=ttk.RIGHT)
        self.facets_combo.current(0)
    def create_facet_table(self, parent, facet_index):
        """
        create facet table
        :param parent:
        :param facet_index:
        :return:
        """
        # Element count combobox for each facet
        header_frame = ttk.Frame(parent)
        header_frame.pack()
        element_count_var = ttk.StringVar(value="1")
        element_count_combo = ttk.Combobox(header_frame,
                                           textvariable=element_count_var,
                                           state="readonly",
                                           values=[str(n) for n in
                                                   range(MIN_FACET_NUM,
                                                         MAX_FACET_NUM + 1)],
                                           width=self.width_facet_combo, )
        element_count_combo.grid(row=0, column=1)
        element_count_combo.current(0)
        element_count_combo.bind("<<ComboboxSelected>>",
                                 lambda e: self.update_table(parent,
                                                             element_count_var.get(),
                                                             facet_index))
        self.facets_elements_combo.append(element_count_combo)
        Label(header_frame, text="No. of elements\nin this facet:",
                  background=self.colors.light,
                  padding=(5, 0)). \
            grid(row=0, column=0, padx=(0, 5), pady=(0, 5))
        # Table for the labels
        parent.table_container = ttk.Frame(parent)
        parent.table_container.pack(fill='both', expand=True)
        self.update_table(parent, element_count_var.get(), facet_index)

    def update_table(self, parent, element_count, facet_index):
        """
        update table with the given element count
        :param parent:
        :param element_count:
        :param facet_index:
        :return:
        """
        # Clear the current table
        for widget in parent.table_container.winfo_children():
            widget.destroy()
        self.facets_entries[facet_index - 1] = []
        # Create the table
        for i in range(int(element_count)):
            Label(parent.table_container, text=f"{i + 1}",
                      background=self.colors.light,
                      padding=(10, 0)).grid(row=i, column=0, padx=(5, 10),
                                            pady=(0, 5))
            entry = ttk.Entry(parent.table_container,
                              width=self.width_facet_element_label_entry)
            entry.grid(row=i, column=1, padx=(0,10))
            entry.insert(0, f"{chr(65 + facet_index - 1)}{i + 1}")  # Default
            self.facets_entries[facet_index - 1].append(entry)
            # label like A1, B2 etc.

    def update_facet_count(self, event=None):
        """
        update the facet count and create new facet frames and tables
        :param event:
        :return:
        """
        # Clear the existing facet frames
        for frame in self.facet_frames:
            frame.destroy()
        self.facet_frames = []
        self.facets_entries = []
        self.facets_elements_combo = []
        # Get the number of facets from the combobox
        facet_count = int(self.facets_combo.get().split()[
                              0]) if self.facets_combo.get() != "No facets" else 0
        # Create new facet frames
        for i in range(facet_count):
            facet_frame = ttk.LabelFrame(self,
                                         text=f"Facet {chr(65 + i)}")
            facet_frame.pack(side='left', fill='y', expand=False, padx=5,
                             pady=5)
            self.facets_entries.append([])
            self.create_facet_table(facet_frame, i + 1)
            self.facet_frames.append(facet_frame)

    def get_facets_details(self):
        facets = []
        for i, _ in enumerate(self.facets_entries):
            facet = []
            for entry in self.facets_entries[i]:
                facet.append(entry.get())
            facets.append(facet)
        return facets

    def get_facets_num(self):
        return len(self.facets_entries)

    def set_facets_num(self, num : int):
        self.facets_combo.current(num)
        self.update_facet_count()

    def set_facets_elements(self, facet_index, elements_num : int):
        """
        set the number of elements for the given facet
        :param facet_index: 1..n
        :param elements_num: 2..9
        :return:
        """
        self.facets_elements_combo[facet_index-1].current(elements_num -
                                                         MIN_FACET_NUM)
        self.update_table(self.facet_frames[facet_index-1], elements_num,
                          facet_index)

    def set_facets_details(self, facet_values : List[List]):
        """
        set the values for the facets
        :param facet_values: list of lists representing the facet values
                             eg. [["A1", "A2", "A3"], ["B1", "B2", "B3"]]
        """
        self.set_facets_num(len(facet_values))
        for facet_i, facet in enumerate(facet_values):
            self.set_facets_elements(facet_i+1, len(facet))
            for element_i, entry in enumerate(self.facets_entries[facet_i]):
                new_value = facet_values[facet_i][element_i]
                entry.delete(0, ttk.END)
                entry.insert(0, new_value)

    def reset(self):
        self.facets_combo.current(0)
        self.update_facet_count()


