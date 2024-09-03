import itertools
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.simpledialog import askstring
import pandas as pd
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from PIL import Image, ImageTk
import os
from lib.utils import *
from lib.fss.recoding import *
from lib.components.form import DataButton
from tktooltip import ToolTip


class DataPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.colors = parent.root.style.colors
        self.create_data_buttons()
        self.vars_i = None
        self.var_details = None
        self.data = None
        self.data_table = None

    def show_data(self, data : pd.DataFrame, var_details=None):
        if var_details:
            self.vars_i = [var['index'] for var in var_details if var['show']]
            self.var_details = var_details
        if self.data_table:
            self.data_table.destroy()
        self.data = data
        self.create_data_table()
        self.set_labels(data.columns)

    def create_data_table(self):
        coldata = [dict(text=col, stretch=True, ) for col in
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
        # # Bind double-click event
        self.data_table.view.unbind('<Button-1>')
        self.data_table.view.bind_all("<Double-1>", self.on_double_click)
        for col in self.data_table.view['columns']:
            self.data_table.view.heading(col, command=lambda: None)
            self.data_table.view.column(col, width=rreal_size(65))
        for i in range(len(self.data.columns)):
            self.data_table.align_heading_center(cid=i)
            self.data_table.align_column_center(cid=i)

    def on_double_click(self, event):
        return
        region = self.data_table.view.identify("region", event.x, event.y)
        column = self.data_table.view.identify_column(event.x)
        if region == "heading":
            # Editing a column name
            col_id = int(column.replace('#', '')) - 1
            old_col_name = self.get_var_label(col_id)
            new_col_name = askstring("Edit Variable Label",
                                     "Edit the variable label:",
                                     initialvalue=old_col_name)
            if new_col_name is not None:
                self.set_var_label(col_id, new_col_name)

    def create_data_buttons(self):
        # Data Buttons Frame
        frame_data_buttons = ttk.Frame(self)
        # Pack the frame for data buttons at the bottom of the screen
        frame_data_buttons.pack(side=tk.BOTTOM, fill='x', padx=rreal_size(15),
                                pady=rreal_size(10))
        # Data Buttons
        self.button_reload = DataButton(frame_data_buttons, text="Reload "
                                                                 "Input",
                                        width=11)
        # self.button_reload.pack(side=tk.LEFT, padx=5)
        self.button_select = DataButton(frame_data_buttons, text="Select "
                                                                 "Vars.",
                                        command=self.select_variables,
                                        bootstyle="secondary")
        # self.button_select.pack(side=tk.RIGHT, padx=5)
        ToolTip(self.button_select, msg="You can return to the previous page "
                                        "in\norder to cancel the selection",
                delay=TOOL_TIP_DELAY)
        self.button_recode = DataButton(frame_data_buttons, text="Recode "
                                                                 "Vars.",
                                        command=self.select_variables,
                                        width=11)
        self.button_recode.pack(side=tk.LEFT, padx=5)
        ToolTip(self.button_recode, msg="different subsets of variables"
                                        "\ncan be recoded differently.",
                delay=TOOL_TIP_DELAY)
        self.button_save = DataButton(frame_data_buttons, text="Save Active "
                                                               "Data To..",
                                      width=rreal_size(18), bootstyle="secondary")
        self.button_save.pack(side=tk.RIGHT, padx=5)

    def select_variables(self, selected_vars: set = None):
        # open a string dialog to select variable columns
        if not selected_vars:
            selected_vars = askstring("Select Variables",
                                      "Enter variable indices:\n"
                                      "e.g. 1-5, 8, 11-13\n")
            selected_vars = self.parse_indices_string(selected_vars)
        if selected_vars:
            for i in selected_vars:
                if i < 1 or i > len(self.data.columns):
                    messagebox.showinfo("Error",
                                        f"Invalid column index {i}. not in range "
                                        f"of 1..{len(self.data.columns)}")
                    return
            if len(selected_vars) < 3:
                messagebox.showinfo("Error", "Please select at least 3 "
                                             "variables.")
                return
            # reset table
            # self.button_reload.invoke()
            # get the data from the table
            data = self.get_all_visible_data()
            labels = self.get_visible_labels()
            new_data = []
            for i in range(len(data)):
                new_data.append([data[i][j - 1] for j in selected_vars])
            selected_labels = [labels[i - 1] for i in selected_vars]
            # create a new dataframe
            selected_data = pd.DataFrame(new_data)
            selected_data.columns = selected_labels
            # show the selected data
            r_selected_var = []
            for i in selected_vars:
                r_selected_var.append(self.vars_i[i-1])
            for var in self.var_details:
                if var['index'] not in r_selected_var:
                    var['show'] = False
                    var['label'] = labels.pop(0)
                else:
                    var['show'] = True
            self.show_data(selected_data, var_details=self.var_details)
            self.set_labels(selected_labels)
            self.select_variables_subset(self.vars_i)

    def select_variables_subset(self, variables_index : list):
        raise Exception("This function should be override")

    def parse_indices_string(self, indices_string) -> set:
        if not indices_string: return set()
        try:
            parsed_indices = indices_string.split(',')
            parsed_indices = [x.strip() for x in parsed_indices]
            parsed_indices = [x.split('-') if '-' in x else x for x in
                              parsed_indices]
            parsed_indices = [
                list(range(int(x[0]), int(x[1]) + 1)) if type(x) is
                                                         list else [
                    int(x)] for x in parsed_indices]
            parsed_indices = set(itertools.chain(*parsed_indices))
            return parsed_indices
        except Exception as e:
            messagebox.showinfo("Error", "Invalid indices string")

    def recode_variables(self, recode_window, recoding_details: dict = None):
        """
        :param recode_window:
        :param recoding_details: {
            "indices_string": self.get_indices() -> indiceString,
            # indices of the columns
            "grouping": int(self.get_grouping()) -> int, # number of groups
            "grouping_type": self.get_grouping_type(),  # ["Percentile", "Equal Intervals", "By Rank"]
            "inverting": self.get_inverting() -> bool  # True or False
        }
        :return:
        """
        if not recoding_details:
            recoding_details = recode_window.get_recoding_details()
        col_indices = self.parse_indices_string(recoding_details[
                                                    'indices_string'])
        recoded = False
        recoded_df = self.data
        for col in [i - 1 for i in col_indices]:
            rec_col = recoded_df.iloc[:, col]
            if recoding_details['grouping']:
                if recoding_details['grouping_type'] == GROUPING_TYPES[0]:
                    rec_col = group_by_precentile(rec_col,
                                                  recoding_details['grouping'])
                elif recoding_details['grouping_type'] == GROUPING_TYPES[1]:
                    rec_col = group_by_equal_range(rec_col,
                                                   recoding_details[
                                                       'grouping'])
                elif recoding_details['grouping_type'] == GROUPING_TYPES[2]:
                    rec_col = group_by_monotonicity(rec_col,
                                                    recoding_details[
                                                        'grouping'])
            recoded = True
            if recoding_details['inverting']:
                rec_col = invert(rec_col)
                recoded = True
            recoded_df.loc[:, recoded_df.columns[col]] = rec_col
        if recoded:
            self.show_data(recoded_df)
        if recode_window:
            recode_window.exit()

    def get_selected_rows(self):
        selected_items = self.data_table.selection()
        selected_data = [self.data_table.item(item, 'values') for item in
                         selected_items]
        return selected_data

    def get_all_visible_data(self):
        if not self.data_table: return None
        data = []
        for i, row in enumerate(self.data_table.tablerows):
            cols = self.data_table.tablecolumns_visible
            cols = list(map(lambda x: x.cid, cols))
            data.append([row.values[int(x)] for x in cols])
        return data

    def get_visible_labels(self):
        """ get the labels from the columns of the datatable"""
        if not self.data_table: return None
        labels = []
        for i, col in enumerate(self.data_table.tablecolumns_visible):
            labels.append(self.get_var_label(i))
        return labels

    def set_labels(self, labels):
        assert len(labels) == len(self.data_table.tablecolumns)
        for i, col in enumerate(self.data_table.tablecolumns):
            self.set_var_label(col.cid, labels[i])

    def get_var_label(self, i):
        return self.data_table.view.heading(i)['text'][3:]

    def set_var_label(self, col_index, label):
        index = f"{int(col_index)+1}. "
        self.data_table.view.heading(col_index, text=index + label)

    def pack(self, kwargs=None, **kw):
        if self.data_table:
            self.data_table.view.bind_all("<Double-1>", self.on_double_click)
        super().pack(kwargs, **kw)

    def pack_forget(self) -> None:
        if self.data_table:
            self.data_table.bind_all("<Double-1>", lambda x: None)
        super().pack_forget()
