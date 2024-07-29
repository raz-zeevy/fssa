import tkinter as tk
from tkinter.simpledialog import askstring
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from lib.components.editable_tree_view import EditableTreeView
from dotmap import DotMap
from lib.components.form import DataButton
from lib.utils import *


# todo: there is a mixup between the sel_var and the var_no
# all works well rn but should be switched in future
LABEL = "Label"
VALID_HIGH = "Valid\nHi. "
VALID_LOW = "Valid\nLo. "
LINE_NO = "Line\nNo."
VAR_NO = "Sel.\nVar."
SEL_VAR = "Var.\nNo."
FIELD_WIDTH = "Field\nWidth"
START_COL = 'Start\nCol.'

PAGE_SIZE = 12
COLUMNS = [
    VAR_NO,
    LINE_NO,
    START_COL,
    FIELD_WIDTH,
    VALID_LOW,
    VALID_HIGH,
    LABEL
]

class ManualFormatPage(ttk.Frame):
    def __init__(self, parent):
        self.data_table = None
        ttk.Frame.__init__(self, parent.root)
        self.coldata = None
        self.are_missing_values = True
        self.colors = parent.root.style.colors
        self.create_data_buttons()
        self.limited_edit_mode = False
        # create entry before the table:
        entry = ttk.Label(self, text="Specify where in the data file the "
                                "variables are located: ")
        entry.pack(side=tk.TOP, fill='x', padx=40, pady=(10, 0))

    def pack(self, kwargs=None, **kw):
        # if self.data_table:
        #     self.data_table.view.bind_all("<Double-1>", self.on_double_click)
        super().pack(kwargs, **kw)

    def pack_forget(self) -> None:
        # if self.data_table:
        #     self.data_table.bind_all("<Double-1>", lambda x: None)
        super().pack_forget()

    ###################
    ###### GUI ########
    ###################

    def create_data_table(self):
        self.limited_edit_mode = False
        if self.data_table is not None:
            self.data_table.destroy()
        self.coldata = COLUMNS
        self.data_table = EditableTreeView(
            self,
            index_col_name=SEL_VAR,
            add_check_box=True,
            columns=self.coldata
        )
        self.data_table.column("Label", stretch=True)
        # self.data_table.place(relx=.5, rely=.49, anchor="center")
        self.data_table.pack(side=tk.TOP, fill=BOTH, expand=True,
                             pady=(10, 10), padx=40)
        self._configure_columns()

    def _configure_columns(self):
        self.data_table.heading("#0", anchor='c')
        self.data_table.column("#0", width=rreal_size(50), anchor='w')
        self.data_table.column(VAR_NO, anchor='c', width=rreal_size(45))
        self.data_table.column(LINE_NO, anchor='c', width=rreal_size(45))
        self.data_table.column(START_COL, anchor='c', width=rreal_size(45))
        self.data_table.column(FIELD_WIDTH, anchor='c', width=rreal_size(50))
        for col in [VALID_LOW, VALID_HIGH,]:
            self.data_table.heading(col, anchor="c")
            self.data_table.column(col, width=rreal_size(45), anchor='c')

    def create_data_buttons(self):
        # Data Buttons Frame
        frame_data_buttons = ttk.Frame(self)
        # Pack the frame for data buttons at the bottom of the screen
        frame_data_buttons.pack(side=tk.BOTTOM, fill='x', padx=10,
                                pady=(0, 20))
        # Data Buttons
        self.button_add_variable = DataButton(frame_data_buttons, text="Add "
                                                                       "Var.",
                                              command=self.add_variable)
        self.button_add_variable.pack(side=tk.LEFT, padx=5)
        self.button_remove_variable = DataButton(frame_data_buttons,
                                                 text="Remove Var.",
                                                 command=self.remove_variable,
                                                 width=11)
        self.button_remove_variable.pack(side=tk.LEFT, padx=5)

    ###################
    #### Get & Set ####
    ###################

    def get_data_format(self):
        """
        Get the data format from the table
        :return: in format of [{line: 1, col: 1, width: 10, label: "Name"}, ...}]
        """
        data_format = []
        for i, row in enumerate(self.data_table.checked_rows()):
            width = int(row[FIELD_WIDTH])
            valid_low = int(row[VALID_LOW])
            valid_high = int(row[VALID_HIGH])
            label = row[LABEL]
            if not self.are_missing_values and width == 2:
                valid_high = 99
            if width not in [1, 2]:
                raise ValueError(f"Row {i+1}: Field width of {width} is not "
                                 f"valid. "
                                 f"Field width must be 1 or 2.")
            if valid_low > valid_high:
                raise ValueError(f"Row {i+1}: Valid low of {valid_low} is "
                                 f"greater than "
                                 f"valid high of {valid_high}.")
            if valid_low < 0 or valid_high > 99:
                raise ValueError(f"Row {i+1}: Valid low of {valid_low} or "
                                 f"valid high of "
                                 f"{valid_high} is not between 0 and 99.")
            if not label.isascii():
                raise ValueError(f'Row {i+1}: Label: "{label}" is not in '
                                 f'ASCII.')
            data_format.append(dict(line=int(row[LINE_NO]),
                                    col=int(row[START_COL]),
                                    width=width,
                                    valid_low=valid_low,
                                    valid_high=valid_high,
                                    label=label))
        return data_format

    def set_limited_edit_mode(self) -> None:
        self.limited_edit_mode = True
        self.button_add_variable.config(state="disabled")
        self.button_remove_variable.config(state="disabled")
        for col in COLUMNS:
            if col not in [VAR_NO, LABEL, VALID_LOW, VALID_HIGH]:
                self.data_table.hide_column(col)

    def unset_limited_edit_mode(self):
        self.limited_edit_mode = False
        self.button_add_variable.config(state="normal")
        self.button_remove_variable.config(state="normal")
        for col in COLUMNS:
            self.data_table.show_column(col)

    def get_labels(self) -> list:
        return [row[LABEL] for row in self.data_table.rows()]

    def get_selected_var_labels(self):
        return [var['Label'] for var in self.data_table.get_checked_rows()]

    def get_len_selected_vars(self):
        return len(self.data_table.get_checked_rows())

    def set_labels(self, list):
        """
        Notice : doesn't change the values in the GUI only in the underlying
        data structure.
        :param list:
        :return:
        """
        assert len(list) == len(self.data_table)
        for i, row in enumerate(self.data_table.row_ids()):
            self.data_table.set(row, LABEL, list[i])

    def select_variables(self, var_indices):
        self.data_table.toggle_all()
        self.data_table.toggle_rows(var_indices)

    def get_vars_valid_values(self):
        all_format = self.get_data_format()
        valid_values = [(var['valid_low'], var['valid_high']) for var in
                        all_format]
        return valid_values

    ######################
    ## Data Table Utils ##
    ######################

    def get_row(self, index) -> dict:
        return self.data_table.get_row(index)

    def row_dict_to_list(self, row_dict):
        return [row_dict.get(col) for col in COLUMNS if
                    row_dict.get(col) is not None]

    def add_row_from_dict(self, row_dict):
        # convert the row_dict to a list of values in the order of the columns
        row_values = self.row_dict_to_list(row_dict)
        self.data_table.add_row(values=row_values)

    #################
    #### Methods ####
    #################

    def load_missing_values(self, are_missing_values):
        if are_missing_values == self.are_missing_values:
            return
        self.create_data_table()
        self.are_missing_values = are_missing_values
        if self.are_missing_values:
            self.data_table.show_column(VALID_LOW)
            self.data_table.show_column(VALID_HIGH)
        else:
            self.data_table.hide_column(VALID_LOW)
            self.data_table.hide_column(VALID_HIGH)

    def remove_variable(self):
        # removes the last row from the table
        self.data_table.remove_row(-1)

    def add_variable(self, line=None, col=None,
                     width=None,
                     valid_low=None, valid_high=None, label=None):

        if self.limited_edit_mode: return

        default_values = {LINE_NO: line, START_COL: col,
                          FIELD_WIDTH: width, VALID_LOW: valid_low,
                          VALID_HIGH: valid_high, LABEL: label}

        def new_row_from_last(**kwargs):
            row_data : dict = self.get_row(-1).copy()
            try:
                row_data[START_COL] = int(row_data[START_COL]) + int(
                    row_data[FIELD_WIDTH])
            except ValueError: pass
            for field in kwargs:
                if kwargs[field] is not None:
                    row_data[field] = kwargs[field]
            return row_data

        def new_row_from_default(**kwargs):
            default_var = {LINE_NO : "1", START_COL : "1",
                               FIELD_WIDTH : "1", VAR_NO : "1",
                               VALID_HIGH : "9", VALID_LOW :"1",
                           LABEL : "var1",}
            for field in kwargs:
                if kwargs[field] is not None:
                    default_var[field] = kwargs[field]
            return default_var

        index = len(self.data_table) + 1
        label = f"var{index}" if not label else label
        #
        if self.data_table.loc(-1):
            new_row : dict = new_row_from_last(**default_values)
        else:
            new_row = new_row_from_default(**default_values)
        new_row[LABEL] = label
        self.add_row_from_dict(new_row)
