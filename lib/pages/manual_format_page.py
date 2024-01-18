import tkinter as tk
from tkinter.simpledialog import askstring
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

PAGE_SIZE = 12


class IndexedTableVIew(Tableview):
    def __init__(self, master=None, **kw):
        Tableview.__init__(self, master=master, **kw)

    def delete_row(self, index=None, iid=None, visible=True):
        Tableview.delete_row(self, index=index, iid=iid, visible=visible)
        self.reindex()

    def delete_rows(self, indices=None, iids=None, visible=True):
        Tableview.delete_rows(self, indices=indices, iids=iids,
                              visible=visible)
        self.reindex()

    def reindex(self):
        for i, row in enumerate(self.tablerows):
            item = self.iidmap[row.iid].iid
            # todo: Maybe should be uncommented not clear
            # row.values[0] = i
            self.view.set(item, column=0, value=i+1)
        self.load_table_data()
class ManualFormatPage(ttk.Frame):
    def __init__(self, parent):
        self.data_table = None
        ttk.Frame.__init__(self, parent.root)
        self.create_navigation()
        self.colors = parent.root.style.colors
        self.create_data_buttons()
        self.create_data_table()

    def create_data_table(self):
        self.coldata = ["#", "Line No.", "Start Col.", "Field Width",
                        "Label"]
        rowdata = []
        self.data_table = IndexedTableVIew(
            master=self,
            coldata=self.coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=False,
            autofit=True,
            autoalign=True,
            bootstyle=PRIMARY,
            stripecolor=(self.colors.light, None),
            pagesize=12
        )
        self.data_table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        self.data_table.bind_all("<Double-1>", self.on_double_click)
        self.data_table.align_column_center(cid=0)
        for i in range(len(self.coldata)):
            self.data_table.align_heading_center(cid=i)
            self.data_table.align_column_center(cid=i)

    def add_variable(self, line_num="", start_col="", field_width="",
                     label=""):
        index = len(self.data_table.iidmap)+1
        if self.data_table.tablerows:
            last_row = self.data_table.tablerows[-1].values
            if not line_num:
                line_num = last_row[1]
            if not start_col:
                start_col = int(last_row[2]) + 1
            if not field_width:
                field_width = last_row[3]
        new_row = [index, line_num, start_col, field_width, label]
        self.data_table.insert_row(index='end', values=new_row)
        self.data_table.load_table_data()
        if len(self.data_table.tablerows) > PAGE_SIZE:
            self.data_table.goto_next_page()

    def on_double_click(self, event):
        item = self.data_table.view.identify('item', event.x, event.y)
        column = self.data_table.view.identify_column(event.x)
        try:
            value = self.data_table.view.item(item, 'values')[int(column[1:]) - 1]
        except IndexError:
            return
        new_value = askstring("Edit Value", "Edit the value:",
                              initialvalue=value)
        if new_value is not None:
            self.data_table.view.set(item, column=column, value=new_value)
            self.data_table.iidmap[item].values[int(column[1:]) - 1] = \
                new_value
    def create_data_buttons(self):
        # Data Buttons Frame
        frame_data_buttons = ttk.Frame(self)
        # Pack the frame for data buttons at the bottom of the screen
        frame_data_buttons.pack(side=tk.BOTTOM, fill='x', padx=10, pady=10)
        # Data Buttons
        self.button_add_variable = ttk.Button(frame_data_buttons, text="Add "
                                                                 "Variable",
                                              command=self.add_variable)
        self.button_add_variable.pack(side=tk.LEFT, padx=5)
        self.button_save = ttk.Button(frame_data_buttons, text="Save", )
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

    def get_data_format(self):
        data_format = []
        for i, row in enumerate(self.data_table.tablerows):
            data_format.append(dict(line = int(row.values[1]),
                                    col = row.values[2],
                                    width = row.values[3],
                                    label = row.values[4]))
        return data_format

    def get_selected_rows(self):
        selected_items = self.data_table.selection()
        selected_data = [self.data_table.item(item, 'values') for item in
                         selected_items]
        return selected_data

    def get_all_visible_data(self):
        data = []
        for i, row in enumerate(self.data_table.tablerows):
            if i == 0: continue
            cols = self.data_table.tablecolumns_visible
            cols = list(map(lambda x: x.cid, cols))[1:]
            data.append([row.values[int(x)] for x in cols])
        return data
