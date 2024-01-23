# controller.py
import os
import pandas as pd
from lib.gui import GUI
from lib.gui import StartPage, DataPage, DimensionsPage, FacetPage, \
    ManualFormatPage, FacetVarPage, HypothesisPage, FacetDimPage
from lib.fss import get_random_data, load_data_file
from lib.fss import create_running_files, run_fortran
from lib.utils import *

START_PAGE_NAME = StartPage.__name__
DATA_PAGE_NAME = DataPage.__name__
DIMENSIONS_PAGE_NAME = DimensionsPage.__name__
FACET_PAGE_NAME = FacetPage.__name__
FACET_VAR_PAGE_NAME = FacetVarPage.__name__
MANUAL_FORMAT_PAGE_NAME = ManualFormatPage.__name__
HYPOTHESIS_PAGE_NAME = HypothesisPage.__name__
FACET_DIM_PAGE_NAME = FacetDimPage.__name__


class Controller:
    def __init__(self):
        self.gui = GUI()
        self.bind_events()
        self.facets_num = 0
        self.data_file_path = None
        self.lines_per_var = None
        self.manual_input = False
        self.navigate_page(MANUAL_FORMAT_PAGE_NAME)
        # self.navigate_page(FACET_PAGE_NAME)
        # self.switch_to_facet_dim_page()

    def bind_events(self):
        self.gui.pages[START_PAGE_NAME]. \
            button_browse.bind("<Button-1>",
                               lambda x: self.load_file())
        self.gui.pages[DATA_PAGE_NAME]. \
            button_save.bind("<Button-1>",
                             lambda x: self.save_data())
        self.gui.pages[DATA_PAGE_NAME]. \
            button_reload.bind("<Button-1>",
                               lambda x: self.load_data_page())
        self.gui.pages[FACET_PAGE_NAME]. \
            facets_combo.bind("<<ComboboxSelected>>",
                              self.on_facet_num_change)
        self.gui.pages[START_PAGE_NAME]. \
            button_manual_input.config(
            command=self.switch_to_manual_format_page)

    def on_facet_num_change(self, event):
        facet_page = self.gui.pages[FACET_PAGE_NAME]
        facet_page.update_facet_count()
        self.load_facet_dim_page()
        self.facets_num = int(facet_page.facets_combo.get().split()[
                                  0]) if facet_page.facets_combo.get() != "No facets" else 0
        if self.facets_num > 0:
            self.gui.button_next.config(state="enabled")
        else:
            self.gui.button_next.config(state="disabled")

    def navigate_page(self, page_name: str):
        # switch page on gui
        self.gui.switch_page(page_name)
        current_page = self.gui.current_page
        # change the binding of the navigation
        if current_page == self.gui.pages['StartPage']:
            self.gui.button_next.config(command=lambda: self.load_data_page())
            self.gui.button_previous.config(state="disabled")
            self.gui.button_run.config(state="disabled")
        if current_page == self.gui.pages['ManualFormatPage']:
            self.gui.button_next.config(command=lambda: self.load_data_page())
            self.gui.button_previous.config(command=lambda: self.navigate_page(
                START_PAGE_NAME))
            self.gui.button_run.config(state="disabled")
            self.gui.button_previous.config(state="enabled")
        elif current_page == self.gui.pages['DataPage']:
            self.gui.button_next.config(command=lambda: self.navigate_page(
                DIMENSIONS_PAGE_NAME))
            if not self.manual_input:
                self.gui.button_previous.config(
                    command=lambda: self.navigate_page(
                        START_PAGE_NAME))
            else:
                self.gui.button_previous.config(
                    command=lambda: self.navigate_page(
                        MANUAL_FORMAT_PAGE_NAME))
            self.gui.button_previous.config(command=lambda: self.navigate_page(
                START_PAGE_NAME))
            self.gui.button_previous.config(state="enabled")
            self.gui.button_run.config(state="disabled")
        elif current_page == self.gui.pages['DimensionsPage']:
            self.gui.button_next.config(command=lambda: self.navigate_page(
                FACET_PAGE_NAME))
            self.gui.button_next.config(state="enabled")
            self.gui.button_previous.config(command=lambda: self.navigate_page(
                DATA_PAGE_NAME))
            self.gui.button_run.config(command=lambda: self.run_fss())
            self.gui.button_run.config(state="enabled")
        elif current_page == self.gui.pages['FacetPage']:
            self.gui.button_next.config(
                command=lambda: self.load_facet_var_page())
            self.gui.button_previous.config(command=lambda: self.navigate_page(
                DIMENSIONS_PAGE_NAME))
            self.gui.button_run.config(state="enabled")
            self.gui.button_run.config(command=lambda: self.run_fss())
            if self.facets_num > 0:
                self.gui.button_next.config(state="enabled")
            else:
                self.gui.button_next.config(state="disabled")
        elif current_page == self.gui.pages['FacetVarPage']:
            self.gui.button_next.config(
                command=lambda: self.navigate_page(HYPOTHESIS_PAGE_NAME))
            self.gui.button_previous.config(command=lambda: self.navigate_page(
                FACET_PAGE_NAME))
        elif current_page == self.gui.pages['HypothesisPage']:
            self.gui.button_next.config(
                command=lambda: self.navigate_page(FACET_DIM_PAGE_NAME))
            self.gui.button_previous.config(command=lambda: self.navigate_page(
                FACET_VAR_PAGE_NAME))
            self.gui.button_next.config(state="enabled")
        elif current_page == self.gui.pages['FacetDimPage']:
            self.gui.button_next.config(state="disabled")
            self.gui.button_previous.config(command=lambda: self.navigate_page(
                HYPOTHESIS_PAGE_NAME))

    def get_valid_values(self):
        all_format = self.gui.pages[
            MANUAL_FORMAT_PAGE_NAME].get_data_format()
        valid_values = [(var['valid_low'], var['valid_high']) for var in
                        all_format]
        return valid_values
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
            if label == f"var{i+1}":
                labels.append("")
            else:
                labels.append(label)
        variables_labels = [{'index': i + 1, 'label': label} for i, label in
                            enumerate(labels)]
        facet_var_details = self.gui.pages[
            FACET_VAR_PAGE_NAME].get_all_var_facets_indices()
        facet_details = self.gui.pages[
            FACET_PAGE_NAME].get_facets_details()
        facet_dim_details = self.gui.pages[
            FACET_DIM_PAGE_NAME].get_facets_dim()
        hypotheses_details = self.gui.pages[
            HYPOTHESIS_PAGE_NAME].get_hypotheses()

        valid_values_range = self.get_valid_values()
        create_running_files(
            nfacet=self.facets_num,
            variables_labels=variables_labels,
            correlation_type=corr_type,
            data_matrix=data,
            min_dim=min_dim, max_dim=max_dim,
            facet_details = facet_details,
            facet_var_details = facet_var_details,
            hypotheses_details = hypotheses_details,
            facet_dim_details = facet_dim_details,
            valid_values_range=valid_values_range
        )
        run_fortran(corr_type)
        print("running")

    def load_data_page(self):
        # load data
        self.data_file_path = self.gui.pages[
            START_PAGE_NAME].get_data_file_path()
        self.lines_per_var = self.gui.pages[
            START_PAGE_NAME].get_lines_per_var()
        called_page = self.gui.current_page.__class__.__name__
        if called_page == START_PAGE_NAME:
            if not self.data_file_path:
                data = get_random_data()
            else:
                data = load_data_file(self.data_file_path,
                                      lines_per_var=self.lines_per_var,
                                      delimiter=self.gui.pages[
                                          'StartPage'].entry_delimiter.get())
        elif called_page == MANUAL_FORMAT_PAGE_NAME:
            data_format = self.gui.pages[
                MANUAL_FORMAT_PAGE_NAME].get_data_format()
            if not data_format:
                raise Exception("Usage Error:\n At least one variable must be"
                                " inserted")
            data = load_data_file(self.data_file_path,
                                  lines_per_var=self.lines_per_var,
                                  manual_format=data_format)
        else:
            raise Exception("Usage Error:\n Unknown page called to switch to"
                            " data page")
        # row
        # add a labels row
        if called_page == MANUAL_FORMAT_PAGE_NAME:
            data.loc[-1] = [row["label"] for row in data_format]
        else:
            data.loc[-1] = [f"var{i + 1}" for i in
                            range(len(data.columns))]
        data.index = data.index + 1  # shifting index
        data.sort_index(inplace=True)
        index_col = list(range(len(data.index)))
        index_col[0] = "labels"
        data.insert(loc=0, column="", value=index_col)
        self.navigate_page(DATA_PAGE_NAME)
        self.gui.pages[DATA_PAGE_NAME].show_data(data)

    def load_facet_var_page(self):
        self.navigate_page(FACET_VAR_PAGE_NAME)
        facets_details = self.gui.pages[FACET_PAGE_NAME].get_facets_details()
        var_labels = self.gui.pages[DATA_PAGE_NAME].get_visible_labels()
        self.gui.pages[FACET_VAR_PAGE_NAME].create_facet_variable_table(
            var_labels=var_labels,
            facet_details=facets_details, )

    def load_facet_dim_page(self):
        max_dim = max(self.gui.pages[DIMENSIONS_PAGE_NAME].get_dimensions())
        min_dim = min(self.gui.pages[DIMENSIONS_PAGE_NAME].get_dimensions())
        self.gui.pages[FACET_DIM_PAGE_NAME].create_facet_dimension_table(
            max_dim=max_dim,
            min_dim=min_dim,
            num_facets=len(
                self.gui.pages[FACET_PAGE_NAME].get_facets_details()))

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

    def switch_to_manual_format_page(self):
        self.manual_input = True
        self.navigate_page(MANUAL_FORMAT_PAGE_NAME)


if __name__ == '__main__':
    controller = Controller()
    controller.run_process()
