#controler.py
import os

import pandas as pd

from lib.gui import GUI
from lib.gui import StartPage, DataPage, DimensionsPage, FacetPage
from lib.fss import get_random_data, load_data_file
from lib.fss import create_running_files
from lib.utils import *

START_PAGE_NAME = StartPage.__name__
DATA_PAGE_NAME = DataPage.__name__
DIMENSIONS_PAGE_NAME = DimensionsPage.__name__
FACET_PAGE_NAME = FacetPage.__name__


class Controller:
    def __init__(self):
        self.gui = GUI()
        self.bind_events()
        self.gui.switch_page(FACET_PAGE_NAME)
        self.data_file_path = None

    def bind_events(self):
        self.gui.pages[START_PAGE_NAME]. \
            button_browse.bind("<Button-1>",
                               lambda x: self.load_file())
        self.gui.pages[START_PAGE_NAME]. \
            button_next.bind("<Button-1>",
                             lambda x: self.switch_to_data_page())
        self.gui.pages[DATA_PAGE_NAME]. \
            button_previous.bind("<Button-1>",
                                 lambda x: self.gui.switch_page(
                                     START_PAGE_NAME))
        self.gui.pages[DATA_PAGE_NAME]. \
            button_next.bind("<Button-1>",
                             lambda x: self.gui.switch_page(
                                 DIMENSIONS_PAGE_NAME))
        self.gui.pages[DATA_PAGE_NAME]. \
            button_save.bind("<Button-1>",
                             lambda x: self.save_data())
        self.gui.pages[DATA_PAGE_NAME]. \
            button_reload.bind("<Button-1>",
                               lambda x: self.switch_to_data_page())
        self.gui.pages[DIMENSIONS_PAGE_NAME]. \
            button_previous.bind("<Button-1>",
                                 lambda x: self.gui.switch_page(
                                     DATA_PAGE_NAME))
        self.gui.pages[DIMENSIONS_PAGE_NAME]. \
            button_next.bind("<Button-1>",
                             lambda x: self.gui.switch_page(
                                 FACET_PAGE_NAME))
        self.gui.pages[FACET_PAGE_NAME]. \
            button_previous.bind("<Button-1>",
                                 lambda x: self.gui.switch_page(
                                     DIMENSIONS_PAGE_NAME))
        self.gui.pages[FACET_PAGE_NAME]. \
            button_run.bind("<Button-1>",
                            lambda x: self.run_fss())

    def run_fss(self):
        # get parameters for fss
        corr_type = self.gui.pages[
            DIMENSIONS_PAGE_NAME].get_correlation_type()
        min_dim = self.gui.pages[
            DIMENSIONS_PAGE_NAME].get_dimensions()[0]
        max_dim = self.gui.pages[
            DIMENSIONS_PAGE_NAME].get_dimensions()[-1]
        data = [row.values for row in self.gui.pages[
                DATA_PAGE_NAME].data_table.tablerows_visible]
        variables_details = [
            {"index": 1, "label": "A", "start_col": 1, "width": 1},
            {"index": 2, "label": "B", "start_col": 2, "width": 1},
            {"index": 3, "label": "C", "start_col": 3, "width": 1},
            {"index": 4, "label": "D", "start_col": 4, "width": 1},
            {"index": 5, "label": "E", "start_col": 5, "width": 1},
            {"index": 6, "label": "F", "start_col": 6, "width": 1}
        ]
        create_running_files(
            variables_details=variables_details,
            correlation_type= corr_type,
            data_matrix=data,
            min_dim=min_dim, max_dim=max_dim,
        )
        print("running")

    def switch_to_data_page(self):
        if not self.data_file_path:
            data = get_random_data()
        else:
            data = load_data_file(self.data_file_path,
                                  self.gui.pages[
                                      'StartPage'].entry_delimiter.get())
        self.gui.switch_page(DATA_PAGE_NAME)
        self.gui.pages[DATA_PAGE_NAME].show_data(data)

    def run_process(self):
        self.gui.run_process()

    def load_file(self):
        def suggest_delimiter(path):
            file_extension = os.path.splitext(path)[
                1].lower()
            if file_extension in ['.csv', '.xlsx', '.xls']:
                self.gui.pages['StartPage'].set_delimiter(",")
            elif file_extension == '.tsv':
                self.gui.pages['StartPage'].set_delimiter('\t')
            else:
                print("unknown del")
                self.gui.pages['StartPage'].set_delimiter(DELIMITER_1_D,
                                                          readonly=False)

        self.gui.pages['StartPage'].browse_file()
        self.data_file_path = self.gui.pages['StartPage'].entry_data_file.get()
        suggest_delimiter(self.data_file_path)

    def save_data(self):
        file_name = self.gui.save_file(file_types=[('csv', '*.csv')],
                                       default_extension=".csv")
        data = pd.DataFrame(self.gui.pages[
                                DATA_PAGE_NAME].get_all_data_from_treeview())
        if file_name:
            try:
                with open(file_name, 'w', newline='',
                          encoding='ascii') as file:
                    file.write(data.to_csv(index=False, header=False, ))
            except UnicodeEncodeError as e:
                self.gui.show_error("Save Error",
                                    "The file contains non-ASCII characters "
                                    "and could not be saved.")
                # Handle the error if your data contains non-ASCII characters

    def shutdown(self):
        # Perform any cleanup necessary before closing the application
        if self.gui:
            # Assuming your GUI class has a root Tkinter window
            self.gui.root.destroy()  # This will close the Tkinter window without exiting Python

if __name__ == '__main__':
    controller = Controller()
    controller.run_process()
