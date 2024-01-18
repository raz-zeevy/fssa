# controller.py
import os
import pandas as pd
from lib.gui import GUI
from lib.gui import StartPage, DataPage, DimensionsPage, FacetPage, ManualFormatPage
from lib.fss import get_random_data, load_data_file
from lib.fss import create_running_files, run_fortran
from lib.utils import *

START_PAGE_NAME = StartPage.__name__
DATA_PAGE_NAME = DataPage.__name__
DIMENSIONS_PAGE_NAME = DimensionsPage.__name__
FACET_PAGE_NAME = FacetPage.__name__
MANUAL_FORMAT_PAGE_NAME = ManualFormatPage.__name__

class Controller:
    def __init__(self):
        self.gui = GUI()
        self.bind_events()
        self.gui.switch_page(FACET_PAGE_NAME)
        self.data_file_path = None
        self.lines_per_var = None

    def bind_events(self):
        self.gui.pages[START_PAGE_NAME]. \
            button_browse.bind("<Button-1>",
                               lambda x: self.load_file())
        self.gui.pages[START_PAGE_NAME]. \
            button_next.bind("<Button-1>",
                             lambda x: self.switch_to_data_page())
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME]. \
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
        data = self.gui.pages[DATA_PAGE_NAME].get_all_visible_data()
        labels = []
        # remove the labels that are default
        for i, label in enumerate(self.gui.pages[
                                    DATA_PAGE_NAME].get_visible_labels()):
            if label == f"var{i}":
                labels.append("")
            else:
                labels.append(label)
        variables_labels = [{'index': i+1, 'label': label} for i, label in
                            enumerate(labels)]
        create_running_files(
            variables_labels=variables_labels,
            correlation_type=corr_type,
            data_matrix=data,
            min_dim=min_dim, max_dim=max_dim,
        )
        run_fortran(corr_type)
        print("running")

    def switch_to_data_page(self):
        # load data
        self.lines_per_var = self.gui.pages[
            START_PAGE_NAME].get_lines_per_var()
        called_page = self.gui.current_page.__class__.__name__
        if called_page == START_PAGE_NAME:
            if not self.data_file_path:
                data = get_random_data()
            else:
                data = load_data_file(self.data_file_path,
                                      lines_per_var=self.lines_per_var,
                                      delimiter = self.gui.pages[
                                          'StartPage'].entry_delimiter.get())
                # add a labels row
                data.loc[-1] = [f"var{i}" for i in
                                range(len(data.columns))]  # adding a
        elif called_page == MANUAL_FORMAT_PAGE_NAME:
            data_format = self.gui.pages[
                MANUAL_FORMAT_PAGE_NAME].get_data_format()
            data = load_data_file(self.data_file_path,
                                  lines_per_var=self.lines_per_var,
                                  manual_format=data_format)
            # add a labels row
            data.loc[-1] = [f"var{i}" for i in
                            range(len(data.columns))]  # adding a
        else:
            raise Exception("Usage Error:\n Unknown page called to switch to"
                            " data page")
        # row
        data.index = data.index + 1  # shifting index
        data.sort_index(inplace=True)
        index_col = list(range(len(data.index)))
        index_col[0] = "labels"
        data.insert(loc=0, column="", value=index_col)
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
                self.gui.pages['StartPage'].set_delimiter(DELIMITER_1_D,
                                                          readonly=False)

        self.gui.pages['StartPage'].browse_file()
        self.data_file_path = self.gui.pages['StartPage'].entry_data_file.get()
        if self.data_file_path:
            self.gui.pages['StartPage'].default_entry_lines()
            suggest_delimiter(self.data_file_path)

    def save_data(self):
        file_name = self.gui.save_file(file_types=[('csv', '*.csv')],
                                       default_extension=".csv")
        data = pd.DataFrame(self.gui.pages[
                                DATA_PAGE_NAME].get_all_visible_data())
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
