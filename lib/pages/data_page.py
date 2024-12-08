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
        self.parent = parent
        self.colors = parent.root.style.colors
        self.create_data_buttons()
        self.vars_i = None
        self.var_details = None
        self.data = None
        self.data_table = None

    def show_data(self, data: pd.DataFrame, var_details=None):
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

    def create_data_buttons(self):
        # Data Buttons Frame
        frame_data_buttons = ttk.Frame(self)
        # Pack the frame for data buttons at the bottom of the screen
        frame_data_buttons.pack(side=tk.BOTTOM, fill='x', padx=rreal_size(15),
                                pady=rreal_size(10))
        
        # Left side buttons
        left_buttons_frame = ttk.Frame(frame_data_buttons)
        left_buttons_frame.pack(side=tk.LEFT)
        
        self.button_recode = DataButton(left_buttons_frame, text="Recode Vars.",
                                        command=self.select_variables,
                                        width=11)
        self.button_recode.pack(side=tk.LEFT, padx=5)
        ToolTip(self.button_recode, msg="different subsets of variables can "
                                        "be\nrecoded differently. If no "
                                        "recoding is\nnecessary press \"Next\"",
                delay=TOOL_TIP_DELAY)

        # Add the new View Present Recoding button
        self.button_recode_history = DataButton(left_buttons_frame, 
                                              text="View Present Recoding",
                                              width=rreal_size(20),
                                              bootstyle="secondary",
                                              command=self.parent.show_recode_history_window)
        self.button_recode_history.pack(side=tk.LEFT, padx=5)
        ToolTip(self.button_recode_history, 
                msg="View the history of all recoding operations\napplied to the current data",
                delay=TOOL_TIP_DELAY)

        # Right side button
        self.button_save = DataButton(frame_data_buttons, text="Save Active Data To..",
                                      width=rreal_size(18),
                                      bootstyle="secondary")
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
                r_selected_var.append(self.vars_i[i - 1])
            for var in self.var_details:
                if var['index'] not in r_selected_var:
                    var['show'] = False
                    var['label'] = labels.pop(0)
                else:
                    var['show'] = True
            self.show_data(selected_data, var_details=self.var_details)
            self.set_labels(selected_labels)
            self.select_variables_subset(self.vars_i)

    def select_variables_subset(self, variables_index: list):
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
        pd.options.mode.chained_assignment = None
        if not recoding_details:
            recoding_details = recode_window.get_recoding_details()
        col_indices = self.parse_indices_string(recoding_details[
                                                    'var_indices_str'])
        recoded = False
        recoded_df = self.data
        for col_i in [i - 1 for i in col_indices]:
            rec_col = recoded_df.iloc[:, col_i]
            for recoding_pair in recoding_details['manual']:
                for old_value in recoding_pair[0].strip().split(','):
                    rec_col = manual_recoding(rec_col, old_value,
                                              recoding_pair[1])
                recoded = True
            if recoding_details['invert']:
                valid_ranges_all = self.get_active_variables_valid_ranges()
                rec_col = invert(rec_col, [valid_ranges_all[col_i]])
                recoded = True
            recoded_df.loc[:, recoded_df.columns[col_i]] = rec_col
        if recoded:
            self.show_data(recoded_df)

    def get_active_variables_valid_ranges(self):
        """
        This function is used by the recording to get the missing values
        of the variable for the inverting option.
        Should be overridden by the controller.
        :return:
        """
        raise Exception("This function should be override")

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
        index = f"{int(col_index) + 1}. "
        self.data_table.view.heading(col_index, text=index + label)

    def pack(self, kwargs=None, **kw):
        if self.data_table:
            self.data_table.view.bind_all("<Double-1>", self.on_double_click)
        super().pack(kwargs, **kw)

    def pack_forget(self) -> None:
        if self.data_table:
            self.data_table.bind_all("<Double-1>", lambda x: None)
        super().pack_forget()
