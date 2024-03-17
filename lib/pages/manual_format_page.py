import tkinter as tk
from tkinter.simpledialog import askstring
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from dotmap import DotMap
from lib.components.form import DataButton

PAGE_SIZE = 12
COLUMNS = DotMap(dict(
    index="Var No.",
    selected="Selected",
    variable_num="Sel'd Var",
    line_num="Line No.",
    field_width="Field Width",
    start_col="Start Col.",
    valid_low="Valid Lo.",
    valid_high="Valid Hi.",
    label="Label"
), _dynamic=False)


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
            self.view.set(item, column=0, value=i + 1)
        self.load_table_data()

class ManualFormatPage(ttk.Frame):
    def __init__(self, parent):
        self.data_table = None
        ttk.Frame.__init__(self, parent.root)
        self.coldata = None
        self.are_missing_values = True
        self.colors = parent.root.style.colors
        self.create_data_buttons()
        self.matrix_edit_mode = False
        self.selected_rows = {}

    def pack(self, kwargs=None, **kw):
        if self.data_table:
            self.data_table.view.bind_all("<Double-1>", self.on_double_click)
        super().pack(kwargs, **kw)

    def pack_forget(self) -> None:
        if self.data_table:
            self.data_table.bind_all("<Double-1>", lambda x: None)
        super().pack_forget()

    ###################
    ###### GUI ########
    ###################

    def create_data_table(self):
        if self.data_table:
            self.data_table.destroy()
        self.coldata = list(COLUMNS.values())
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
            pagesize=12,
        )
        self.data_table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        self.data_table.bind_all("<Double-1>", self.on_double_click)
        self.data_table.bind_all("<Button-1>", self.on_click)
        self.data_table.align_column_center(cid=0)
        for i in range(len(self.coldata)):
            self.data_table.align_heading_center(cid=i)
            self.data_table.align_column_center(cid=i)

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
            data_format.append(dict(line=int(row.values[1]),
                                    col=int(row.values[2]),
                                    width=width,
                                    valid_low=valid_low,
                                    valid_high=valid_high,
                                    label=row.values[6]))
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

    def set_matrix_edit_mode(self) -> None:
        if not self.matrix_edit_mode:
            self.matrix_edit_mode = True
            self.button_add_variable.config(state="disabled")
            self.button_remove_variable.config(state="disabled")
            for i in range(1, len(self.coldata) - 1):
                self.data_table.tablecolumns[i].hide()

    def get_labels(self) -> list:
        return [row.values[len(self.coldata) - 1] for row in
                self.data_table.tablerows]

    def set_labels(self, list):
        """
        Notice : doesn't change the values in the GUI only in the underlying
        data structure.
        :param list:
        :return:
        """
        assert len(list) == len(self.data_table.tablerows)
        for i, row in enumerate(self.data_table.tablerows):
            row.values[len(self.coldata) - 1] = list[i]

    def get_vars_valid_values(self):
        all_format = self.get_data_format()
        valid_values = [(var['valid_low'], var['valid_high']) for var in
                        all_format]
        return valid_values

    ######################
    ## Data Table Utils ##
    ######################

    def get_col_index_string(self, col_name) -> str:
        """ returns: a column index string in the format of "#<index>"""
        return "#" + str(self.coldata.index(col_name) + 1)

    def get_col_index(self, col_name) -> int:
        """ returns: a column index in the format of "#<index>"""
        return list(COLUMNS.keys()).index(col_name)

    def get_row(self, index) -> dict:
        if index < 0 :
            index = len(self.data_table.tablerows) + index
        if index < 0 or index >= len(self.data_table.tablerows):
            raise IndexError(f"Index {index} is out of range."
                             f"table length is {len(self.data_table.tablerows)}.")
        visible_columns = self.data_table.tablecolumns_visible
        row_data = self.data_table.tablerows[index].values
        row = {}
        for i, col in enumerate(visible_columns):
            key = list(COLUMNS.keys())[int(col.cid)]
            row[key] = row_data[i]
        row['selected'] = row['selected'] == "☑"
        return row

    def set_row(self, index, **kwargs):
        row = self.get_row(index)
        for key in kwargs:
            if key == "selected":
                row[key] = "☑" if kwargs[key] else "☐"
            else:
                row[key] = kwargs[key]
        self.data_table.tablerows[index].values = self.row_dict_to_list(row)
        self.data_table.load_table_data()

    def row_dict_to_list(self, row_dict):
        return [row_dict.get(col) for col in COLUMNS.keys() if
                    row_dict.get(col) is not None]

    def add_row_from_dict(self, row_dict):
        # convert the row_dict to a list of values in the order of the columns
        row_values = self.row_dict_to_list(row_dict)
        row_values[self.get_col_index('selected')] = "☑" if row_dict[
            'selected'] else "☐"
        self.data_table.insert_row(index='end', values=row_values)
        self.data_table.load_table_data()

    #################
    #### Methods ####
    #################

    def load_missing_values(self, are_missing_values):
        if are_missing_values == self.are_missing_values:
            return
        self.create_data_table()
        self.are_missing_values = are_missing_values
        if self.are_missing_values:
            self.data_table.tablecolumns[-2].show()
            self.data_table.tablecolumns[-3].show()
        else:
            self.data_table.tablecolumns[-2].hide()
            self.data_table.tablecolumns[-3].hide()

    def remove_variable(self):
        # removes the last row from the table
        if self.data_table.tablerows:
            self.data_table.delete_row(iid=
                                       self.data_table.tablerows[-1].iid,
                                       visible=False)
            # it is mandatory to check both because the interface is bugged
            if len(self.data_table.tablerows) == PAGE_SIZE:
                self.data_table.goto_first_page()
            elif len(self.data_table.tablerows) % PAGE_SIZE == 0:
                self.data_table.goto_prev_page()

    def add_variable(self, line_num=None, start_col=None,
                     field_width=None,
                     valid_low=None, valid_high=None, label=None,
                     selected=True):
        def new_row_from_last(**kwargs):
            row_data : dict = self.get_row(-1).copy()
            try:
                row_data['start_col'] = int(row_data['start_col']) + int(
                    row_data['field_width'])
                row_data['variable_num'] = int(row_data['variable_num']) + 1
                row_data['index'] = int(row_data['index']) + 1
            except ValueError: pass
            for field in kwargs:
                if kwargs[field] is not None:
                    row_data[field] = kwargs[field]
            return row_data

        def new_row_from_default(**kwargs):
            default_var = dict(index="1", line_num="1", start_col="1",
                               field_width="1", variable_num="1",
                               valid_low="1", valid_high="9", label="var1",
                               selected=True)
            for field in kwargs:
                if kwargs[field] is not None:
                    default_var[field] = kwargs[field]
            return default_var

        index = len(self.data_table.iidmap) + 1
        label = f"var{index}" if not label else label
        #
        if self.data_table.tablerows and self.data_table.tablerows[-1].values:
            new_row : dict = new_row_from_last(line_num=line_num,
                                               start_col=start_col, field_width=field_width,
                     valid_low=valid_low, valid_high=valid_high, label=label,
                     selected=selected)
        else:
            new_row = new_row_from_default(line_num=line_num, start_col=start_col, field_width=field_width,
                     valid_low=valid_low, valid_high=valid_high, label=label,
                     selected=selected)
        self.add_row_from_dict(new_row)
        # create a new checkbutton for the new row, set it to be selected and
        # pack it in the "selected" column in the new row
        if len(self.data_table.tablerows) > PAGE_SIZE:
            self.data_table.goto_next_page()

    def on_double_click(self, event):
        item = self.data_table.view.identify('item', event.x, event.y)
        column_key = self.data_table.view.identify_column(event.x)
        column_i = int(column_key[1:])
        if column_i == 1: return
        if self.matrix_edit_mode:
            if column_i != 2:
                return
            column_i = len(self.coldata)
        if not self.are_missing_values and column_i > 4:
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

    def on_click(self, event):
        # Identify the row and column clicked
        row_id_string = self.data_table.view.identify_row(event.y)
        column = self.data_table.view.identify_column(event.x)
        region = self.data_table.view.identify("region", event.x, event.y)
        if region != "cell" or column != self.get_col_index_string(
                COLUMNS['selected']):
            return
        row_id = int(row_id_string[1:]) - 1
        row_data = self.get_row(int(row_id))
        self.set_row(row_id, selected=not row_data['selected'])
