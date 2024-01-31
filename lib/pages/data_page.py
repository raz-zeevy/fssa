import tkinter as tk
from tkinter import filedialog
from tkinter.simpledialog import askstring

import pandas as pd
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from PIL import Image, ImageTk
import os

from lib.components.form import DataButton


class DataPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
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
            paginated=False,
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
        self.data_table.view.unbind('<Button-1>')
        self.data_table.view.bind_all("<Double-1>", self.on_double_click)
        for col in self.data_table.view['columns']:
            self.data_table.view.heading(col, command=lambda: None)
        for i in range(len(self.data.columns)):
            self.data_table.align_heading_center(cid=i)
            self.data_table.align_column_center(cid=i)
        # # Pack the Treeview last so it fills the remaining space
        # self.data_table.pack(side=ttk.LEFT, fill='both', expand=True)

    def on_double_click(self, event):
        region = self.data_table.view.identify("region", event.x, event.y)
        column = self.data_table.view.identify_column(event.x)
        if region == "heading":
            # Editing a column name
            old_col_name = self.data_table.view.heading(column)['text']
            new_col_name = askstring("Edit Variable Label",
                                     "Edit the variable label:",
                                     initialvalue=old_col_name)
            if new_col_name is not None:
                self.data_table.view.heading(column, text=new_col_name)
    def create_data_buttons(self):
        # Data Buttons Frame
        frame_data_buttons = ttk.Frame(self)
        # Pack the frame for data buttons at the bottom of the screen
        frame_data_buttons.pack(side=tk.BOTTOM, fill='x', padx=10, pady=10)
        # Data Buttons
        self.button_reload = DataButton(frame_data_buttons, text="Reload",)
        self.button_reload.pack(side=tk.LEFT, padx=5)
        self.button_save = DataButton(frame_data_buttons, text="Save",)
        self.button_save.pack(side=tk.LEFT, padx=5)


    def get_selected_rows(self):
        selected_items = self.data_table.selection()
        selected_data = [self.data_table.item(item, 'values') for item in
                         selected_items]
        return selected_data

    def get_all_visible_data(self):
        data = []
        for i,row in enumerate(self.data_table.tablerows):
            cols = self.data_table.tablecolumns_visible
            cols = list(map(lambda x: x.cid, cols))
            data.append([row.values[int(x)] for x in cols])
        return data

    def get_visible_labels(self):
        """ get the labels from the columns of the datatable"""
        labels = []
        for i, col in enumerate(self.data_table.tablecolumns_visible):
            labels.append(self.data_table.view.heading(i)['text'])
        return labels

    def pack(self, kwargs=None, **kw):
        if self.data_table:
            self.data_table.view.bind_all("<Double-1>", self.on_double_click)
        super().pack(kwargs, **kw)

    def pack_forget(self) -> None:
        if self.data_table:
            self.data_table.bind_all("<Double-1>", lambda x : None)
        super().pack_forget()