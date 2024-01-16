import tkinter as tk
from tkinter import filedialog
from tkinter.simpledialog import askstring

import pandas as pd
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from PIL import Image, ImageTk
import os

class DataPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.create_navigation()
        self.colors = parent.root.style.colors
        self.create_data_buttons()
        self.data = None
        self.data_table = None

    def show_data(self, data):
        if self.data_table:
            self.data_table.destroy()
        self.data = data
        self.create_data_table()
    def create_data_table(self):
        coldata = [dict(text=col, stretch=False, ) for col in
                   self.data.columns]
        rowdata = [row for row in self.data.values]
        self.data_table = Tableview(
            master=self,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=False,
            autofit=True,
            autoalign=True,
            bootstyle=PRIMARY,
            stripecolor=(self.colors.light, None),
        )
        self.data_table.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Data Table Frame
        # frame_data_table = ttk.Frame(self)
        # frame_data_table.pack(fill='both', expand=True, padx=10, pady=10)

        # # Data Table
        # self.data_table = ttk.tableview.Tableview(frame_data_table)
        #
        # # Vertical Scrollbar
        # v_scrollbar = ttk.Scrollbar(frame_data_table, orient="vertical",
        #                             command=self.data_table.yview)
        # v_scrollbar.pack(side='right', fill='y')
        # self.data_table.configure(yscrollcommand=v_scrollbar.set)
        #
        # # Horizontal Scrollbar
        # h_scrollbar = ttk.Scrollbar(frame_data_table, orient="horizontal",
        #                             command=self.data_table.xview)
        # h_scrollbar.pack(side='bottom', fill='x')
        # self.data_table.configure(xscrollcommand=h_scrollbar.set)
        #
        # # Data Table Columns
        # self.data_table['columns'] = list(self.data.columns)
        # self.data_table['show'] = 'headings'
        # for column in self.data_table['columns']:
        #     self.data_table.heading(column, text=column)
        #     self.data_table.column(column,
        #                            width=100)  # Adjust column width as needed
        #
        # # Data Table Rows
        # for row in self.data.iterrows():
        #     self.data_table.insert('', 'end', values=list(row[1]))
        #
        # # Bind double-click event
        self.data_table.bind_all("<Double-1>", self.on_double_click)
        # # Pack the Treeview last so it fills the remaining space
        # self.data_table.pack(side=ttk.LEFT, fill='both', expand=True)

    def on_double_click(self, event):
        item = self.data_table.view.identify('item', event.x, event.y)
        column = self.data_table.view.identify_column(event.x)
        value = self.data_table.view.item(item, 'values')[int(column[1:]) - 1]
        new_value = askstring("Edit Value", "Edit the value:",
                              initialvalue=value)
        if new_value is not None:
            self.data_table.view.set(item, column=column, value=new_value)
    def create_data_buttons(self):
        # Data Buttons Frame
        frame_data_buttons = ttk.Frame(self)
        # Pack the frame for data buttons at the bottom of the screen
        frame_data_buttons.pack(side=tk.BOTTOM, fill='x', padx=10, pady=10)
        # Data Buttons
        self.button_reload = ttk.Button(frame_data_buttons, text="Reload")
        self.button_reload.pack(side=tk.LEFT, padx=5)
        self.button_save = ttk.Button(frame_data_buttons, text="Save",)
        self.button_save.pack(side=tk.LEFT, padx=5)

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
        self.button_next = ttk.Button(center_frame, text="Next")
        self.button_next.pack(side=ttk.LEFT, padx=5)
        # self.button_run = ttk.Button(center_frame, text="Run")
        # self.button_run.pack(side=ttk.LEFT, padx=5)

        # Additional method to get selected rows

    def get_selected_rows(self):
        selected_items = self.data_table.selection()
        selected_data = [self.data_table.item(item, 'values') for item in
                         selected_items]
        return selected_data

    def get_all_data_from_treeview(self):
        # Get all children (rows) of the treeview
        rows = self.data_table.view.get_children()

        # List to store all data
        all_data = []

        # Iterate over each row and fetch the data
        for row in rows:
            row_data = self.data_table.view.item(row)['values']
            all_data.append(row_data)

        return all_data