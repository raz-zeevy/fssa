import tkinter as tk
from tkinter.simpledialog import askstring
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

from lib.components.form import DataButton

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
        self.coldata = None
        self.are_missing_values = True
        self.colors = parent.root.style.colors
        self.create_data_buttons()
        self.create_data_table()

    def create_data_table(self):
        self.coldata = ["#", "Line No.", "Start Col.", "Field Width",
                        "Valid Lo.", "Valid Hi.",
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

    def load_missing_values(self, are_missing_values):
        self.are_missing_values = are_missing_values
        if self.are_missing_values:
            self.data_table.tablecolumns[-2].show()
            self.data_table.tablecolumns[-3].show()
        else:
            self.data_table.tablecolumns[-2].hide()
            self.data_table.tablecolumns[-3].hide()

    def add_variable(self, line_num="", start_col="", field_width="",
                     valid_low="", valid_high="", label=""):
        index = len(self.data_table.iidmap)+1
        label = f"var{index}" if not label else label
        def new_row_from_last(line_num_="", start_col_="", field_width_="",
                     valid_low_="", valid_high_="", label_=""):
            line_num = line_num_ if line_num_ else last_row[1]
            start_col = start_col_ if start_col_ else int(last_row[2]) + \
                                                     int(last_row[3])
            field_width = field_width_ if field_width_ else last_row[3]
            valid_low = valid_low_ if valid_low_ else last_row[4]
            valid_high = valid_high_ if valid_high_ else last_row[5]
            return [index, line_num, start_col, field_width, valid_low,
                    valid_high, label]

        def new_row_from_default(line_num_="", start_col_="", field_width_="",
                                 valid_low_="", valid_high_="", label_=""):
            line_num = line_num_ if line_num_ else '1'
            start_col = start_col_ if start_col_ else '1'
            field_width = field_width_ if field_width_ else '1'
            valid_low = valid_low_ if valid_low_ else '1'
            valid_high = valid_high_ if valid_high_ else '9'
            return [index, line_num, start_col, field_width, valid_low,
                    valid_high, label]

        if self.data_table.tablerows and self.data_table.tablerows[-1].values:
            last_row = self.data_table.tablerows[-1].values
            new_row = new_row_from_last(line_num, start_col, field_width,
                                        valid_low, valid_high, label)
        else:
            new_row = new_row_from_default(line_num, start_col,
                                           field_width,
                                           valid_low, valid_high, label)
        self.data_table.insert_row(index='end', values=new_row)
        self.data_table.load_table_data()
        if len(self.data_table.tablerows) > PAGE_SIZE:
            self.data_table.goto_next_page()

    def on_double_click(self, event):
        item = self.data_table.view.identify('item', event.x, event.y)
        column_key = self.data_table.view.identify_column(event.x)
        column_i = int(column_key[1:])
        if not self.are_missing_values:
            column_i += 2
        try:
            value = self.data_table.view.item(item, 'values')[column_i - 1]
        except IndexError:
            return
        new_value = askstring("Edit Value", "Edit the value:",
                              initialvalue=value)
        if new_value is not None:
            self.data_table.view.set(item, column=column_key, value=new_value)
            self.data_table.iidmap[item].values[column_i - 1] = new_value
    def create_data_buttons(self):
        # Data Buttons Frame
        frame_data_buttons = ttk.Frame(self)
        # Pack the frame for data buttons at the bottom of the screen
        frame_data_buttons.pack(side=tk.BOTTOM, fill='x', padx=10, pady=10)
        # Data Buttons
        self.button_add_variable = DataButton(frame_data_buttons, text="Add "
                                                                 "Variable",
                                              command=self.add_variable)
        self.button_add_variable.pack(side=tk.LEFT, padx=5)
        self.button_save = DataButton(frame_data_buttons, text="Save", )
        self.button_save.pack(side=tk.LEFT, padx=5)

    def get_data_format(self):
        """
        Get the data format from the table
        :return: in format of [{line: 1, col: 1, width: 10, label: "Name"}, ...}]
        """
        data_format = []
        for i, row in enumerate(self.data_table.tablerows):
            width = int(row.values[3])
            valid_low = int(row.values[4])
            valid_high = int(row.values[5])
            label = row.values[6]
            if not self.are_missing_values and width == 2:
                valid_high = 99
            if width not in [1, 2]:
                raise ValueError(f"Field width of {width} is not valid. "
                                 f"Field width must be 1 or 2.")
            if valid_low > valid_high:
                raise ValueError(f"Valid low of {valid_low} is greater than "
                                 f"valid high of {valid_high}.")
            if valid_low < 0 or valid_high > 99:
                raise ValueError(f"Valid low of {valid_low} or valid high of "
                                 f"{valid_high} is not between 0 and 99.")
            if not label.isascii():
                raise ValueError(f'Label: "{label}" is not in ASCII.')
            data_format.append(dict(line = int(row.values[1]),
                                    col = int(row.values[2]),
                                    width = width,
                                    valid_low = valid_low,
                                    valid_high = valid_high,
                                    label = row.values[6]))
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