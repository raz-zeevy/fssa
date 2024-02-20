# controller.py
import warnings

import pandas as pd
from lib.components.shapes import ShapeFactory
from lib.gui import GUI
from lib.fss.fss_module import get_random_data, load_recordad_data, \
    load_matrix_data, create_matrix_running_files
from lib.fss.fss_module import create_running_files, run_fortran
from lib.utils import *


class Controller:
    def __init__(self):
        self.gui = GUI()
        self.bind_gui_events()
        self.navigator = self.init_navigator()
        ###
        self.init_controller_attributes()
        self.manual_input = False
        self.matrix_input = False
        self.are_missing_values = None
        self.lines_per_var = None
        self.output_path = None
        self.facets_num = 0
        self.max_dim = None
        self.min_dim = None
        #
        self.gui.switch_page(START_PAGE_NAME)
        #
        # self.start_fss()
        # self.navigate_page(DATA_PAGE_NAME)
        # self.navigate_page(FACET_PAGE_NAME)
        # self.navigate_page(INPUT_PAGE_NAME)
        # self.switch_to_facet_dim_page()

        # Override the default showwarning method with your custom one
        warnings.showwarning = self.custom_show_warning

    def custom_show_warning(self, message, category, filename, lineno,
                            file=None,
                            line=None):
        # Convert the warning message to a string and display it using your GUI
        warning_msg = f"{message}"
        # Assuming you have a GUI instance available as `self.gui`
        self.gui.show_warning("Warning", warning_msg)

    def init_controller_attributes(self):
        self.data_file_path = None
        self.var_labels = None
        self.facet_var_details = None
        self.facet_details = []
        self.facet_dim_details = None
        #
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].create_data_table()
        self.gui.pages[INPUT_PAGE_NAME].reset_entries()

    def init_navigator(self):
        navigator = Navigator(self.gui.pages)
        navigator.hide_page(MANUAL_FORMAT_PAGE_NAME)
        navigator.add_block(FACET_PAGE_NAME)
        return navigator

    def error_handler(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                if IS_PRODUCTION():
                    if isinstance(e, DataLoadingException):
                        self.gui.show_error("Data Loading Error",
                                            "Failed to automatically parse "
                                            "the data file variables. Please "
                                            "check again "
                                            "that the data file matches the "
                                            "options you selected, "
                                            "or if you use recorded data chose"
                                            " the manual parsing option.")
                    else:
                        self.gui.show_error("Error Occurred", str(e))
                else:
                    raise e

        return wrapper

    def bind_keys(self):
        self.gui.root.bind("<F1>", lambda x: self.show_help())

    def bind_gui_events(self):
        # Matrix page
        self.gui.pages[MATRIX_INPUT_PAGE_NAME]. \
            button_browse.bind("<Button-1>",
                               lambda x: self.load_matrix_file())
        # input page
        self.gui.pages[INPUT_PAGE_NAME]. \
            button_browse.bind("<Button-1>",
                               lambda x: self.load_recorded_data_file())
        self.gui.pages[INPUT_PAGE_NAME].check_box_manual_input.config(
            command=self.on_manual_input_change
        )
        # data page
        self.gui.pages[DATA_PAGE_NAME]. \
            button_save.bind("<Button-1>",
                             lambda x: self.save_data())
        self.gui.pages[DATA_PAGE_NAME]. \
            button_reload.configure(command=self.load_data_page)
        self.gui.pages[FACET_PAGE_NAME]. \
            facets_combo.bind("<<ComboboxSelected>>",
                              self.on_facet_num_change)
        # bind start page buttons
        self.gui.pages[START_PAGE_NAME].button_recorded_data.configure(
            command=lambda: self.start_fss(matrix=False))
        self.gui.pages[START_PAGE_NAME].button_matrix_data.configure(
            command=lambda: self.start_fss(matrix=True))
        self.gui.pages[START_PAGE_NAME].button_info.configure(
            command=lambda: self.show_help("what_is_fssa"))
        # bind gui getters
        self.gui.get_input_file_name = lambda: os.path.basename(
            self.data_file_path)

    def bind_menu(self):
        self.gui.file_menu.entryconfig("Run", command=self.run_button_click)
        self.gui.input_data_menu.entryconfig("Data",
                                             command=self.load_data_page)
        self.gui.input_data_menu.entryconfig("Variables",
                                             command=self.switch_to_manual_format_page)
        self.gui.diagram_2d_menu.entryconfig("No Facet", command=lambda:
        self.show_diagram_window(2, None))
        self.gui.diagram_2d_menu.entryconfig("Facet A", command=lambda:
        self.show_diagram_window(2, 1))
        self.gui.diagram_2d_menu.entryconfig("Facet B", command=lambda:
        self.show_diagram_window(2, 2))
        self.gui.diagram_2d_menu.entryconfig("Facet C", command=lambda:
        self.show_diagram_window(2, 3))
        self.gui.diagram_2d_menu.entryconfig("Facet D", command=lambda:
        self.show_diagram_window(2, 4))
        self.gui.diagram_3d_menu.entryconfig("No Facet", command=lambda:
        self.show_diagram_window(3, None))
        self.gui.diagram_3d_menu.entryconfig("Facet A", command=lambda:
        self.show_diagram_window(3, 1))
        self.gui.diagram_3d_menu.entryconfig("Facet B", command=lambda:
        self.show_diagram_window(3, 2))
        self.gui.diagram_3d_menu.entryconfig("Facet C", command=lambda:
        self.show_diagram_window(3, 3))
        self.gui.diagram_3d_menu.entryconfig("Facet D", command=lambda:
        self.show_diagram_window(3, 3))

    def start_fss(self, matrix=False):
        self.navigator.pop_page(0)
        if matrix:
            self.matrix_input = True
            self.navigator.hide_page(INPUT_PAGE_NAME)
            self.navigator.hide_page(DATA_PAGE_NAME)
            self.navigator.show_page(MANUAL_FORMAT_PAGE_NAME)
        else:
            self.navigator.hide_page(MATRIX_INPUT_PAGE_NAME)
        self.gui.start_fss()
        self.bind_menu()
        self.bind_keys()
        # bind the navigation buttons
        self.gui.button_run.config(command=lambda: self.run_button_click())
        self.gui.button_next.config(command=self.next_page)
        self.gui.button_previous.config(command=self.previous_page)
        # start
        self.navigate_page(self.navigator.get_current())

    def enable_run(self):
        self.gui.file_menu.entryconfig("Run", state="normal")
        self.gui.button_run.config(state="normal")

    def disable_run(self):
        self.gui.file_menu.entryconfig("Run", state="disabled")
        self.gui.button_run.config(state="disabled")

    def open_results(self):
        os.startfile(self.output_path)

    def enable_view_results(self):
        self.gui.view_menu.entryconfig("Output File", state="normal")
        self.gui.view_menu.entryconfig("Output File",
                                       command=self.open_results)
        if self.min_dim <= 2:
            self.gui.view_menu.entryconfig("2D Diagram ", state="normal")
        if self.max_dim >= 3:
            self.gui.view_menu.entryconfig("3D Diagram ", state="normal")
        for menu in [self.gui.diagram_2d_menu, self.gui.diagram_3d_menu]:
            for i in range(self.facets_num):
                menu.entryconfig("Facet " + chr(65 + i), state="normal")

    def enable_view_input(self):
        def view_input():
            os.startfile(self.data_file_path)

        self.gui.view_menu.entryconfig("Input File", state="normal")
        self.gui.view_menu.entryconfig("Input File", command=view_input)

    def on_facet_num_change(self, event):
        facet_page = self.gui.pages[FACET_PAGE_NAME]
        facet_page.update_facet_count()
        self.facets_num = int(facet_page.facets_combo.get().split()[
                                  0]) if facet_page.facets_combo.get() != "No facets" else 0
        if self.facets_num > 0:
            self.load_facet_dim_page()
            self.load_hypothesis_page()
            self.navigator.remove_block(FACET_PAGE_NAME)
        else:
            self.navigator.add_block(FACET_PAGE_NAME)
            self.gui.button_run.update()
        self.update_navigation_buttons()

    def on_manual_input_change(self):
        self.gui.pages[
            INPUT_PAGE_NAME].on_manual_input_change()
        self.manual_input = self.gui.pages[
            INPUT_PAGE_NAME].manual_input_var.get()
        if self.manual_input:
            self.navigator.show_page(MANUAL_FORMAT_PAGE_NAME)
        else:
            self.navigator.hide_page(MANUAL_FORMAT_PAGE_NAME)

    @error_handler
    def next_page(self):
        cur_page = self.navigator.get_current()
        next_page = self.navigator.get_next()
        # Input Page
        if cur_page == INPUT_PAGE_NAME:
            Validator.validate_input_page(
                self.gui.pages[INPUT_PAGE_NAME].get_data_file_path())
            self.manual_input = self.gui.pages[
                INPUT_PAGE_NAME].manual_input_var.get()
            self.are_missing_values = self.gui.pages[
                INPUT_PAGE_NAME].missing_value_var.get()
            if self.manual_input:
                self.gui.pages[MANUAL_FORMAT_PAGE_NAME].load_missing_values(
                    self.are_missing_values)
                self.navigator.show_page(MANUAL_FORMAT_PAGE_NAME)
            else:
                self.navigator.hide_page(MANUAL_FORMAT_PAGE_NAME)
        # Matrix Input page
        if cur_page == MATRIX_INPUT_PAGE_NAME:
            self.load_matrix()
        # Manual Format Page
        if cur_page == MANUAL_FORMAT_PAGE_NAME and \
            next_page == DATA_PAGE_NAME:
            Validator.validate_manual_input(self.gui.pages[
                                                MANUAL_FORMAT_PAGE_NAME].get_data_format())
            self.manual_input = True
        # Data Page
        if cur_page == DATA_PAGE_NAME:
            Validator.validate_data_page(
                data=self.gui.pages[DATA_PAGE_NAME].get_all_visible_data(),
                labels=self.gui.pages[DATA_PAGE_NAME].get_visible_labels()
            )
            self.navigator.show_page(DIMENSIONS_PAGE_NAME)
        # Dimension Page
        if cur_page == DIMENSIONS_PAGE_NAME:
            cur_dims = self.gui.pages[
                DIMENSIONS_PAGE_NAME].get_dimensions()
            if cur_dims[0] != self.min_dim or cur_dims[-1] != self.max_dim:
                self.min_dim, self.max_dim = cur_dims[0], cur_dims[-1]
                if self.facets_num > 0:
                    self.load_facet_dim_page()
                    if self.min_dim > 2:
                        self.navigator.hide_page(HYPOTHESIS_PAGE_NAME)
                    else:
                        self.navigator.show_page(HYPOTHESIS_PAGE_NAME)
        # Facet Page
        if cur_page == FACET_PAGE_NAME:
            if self.facet_details:
                cur_facet_details = self.gui.pages[
                    FACET_PAGE_NAME].get_facets_details()
                if cur_facet_details == self.facet_details:
                    self.navigate_page(next_page)
                    return
            self.load_facet_var_page()
            self.facet_details = self.gui.pages[
                FACET_PAGE_NAME].get_facets_details()
        # Facet Var Page
        if cur_page == FACET_VAR_PAGE_NAME:
            Validator.validate_facet_var_page(self.gui.pages[
                                                  FACET_VAR_PAGE_NAME].get_all_var_facets_indices())

        if next_page == DATA_PAGE_NAME:
            self.load_data_page()
        self.navigate_page(next_page)

    def load_matrix(self):
        self.data_file_path = self.gui.pages[
            MATRIX_INPUT_PAGE_NAME].get_data_file_path()
        Validator.validate_input_page(self.data_file_path)
        matrix_details = self.gui.pages[MATRIX_INPUT_PAGE_NAME]. \
            get_matrix_details()
        try:
            self.matrix = load_matrix_data(self.data_file_path,
                                           matrix_details)
        except:
            raise DataLoadingException("Error loading matrix data")
        manual_input = self.gui.pages[MANUAL_FORMAT_PAGE_NAME]
        for i in range(len(self.matrix)):
            manual_input.add_variable("","","","","")
        manual_input.set_matrix_edit_mode()
        self.gui.pages[DIMENSIONS_PAGE_NAME].set_matrix_mode()
    def previous_page(self):
        previous_page = self.navigator.get_prev()
        self.navigate_page(previous_page)

    def update_navigation_buttons(self):
        # change the state of previous and next buttons
        if self.navigator.get_prev():
            self.gui.button_previous_config(state="normal")
        else:
            self.gui.button_previous_config(state="disabled")
        if self.navigator.get_next():
            self.gui.button_next_config(state="normal")
        else:
            self.gui.button_next_config(state="disabled")

    def navigate_page(self, page_name: str):
        # switch page on gui
        self.gui.switch_page(page_name)
        self.navigator.set_page(page_name)

        # change the state of previous and next buttons
        self.update_navigation_buttons()

        # change the state of the run button
        if page_name in [INPUT_PAGE_NAME, MANUAL_FORMAT_PAGE_NAME,
                         DATA_PAGE_NAME, DIMENSIONS_PAGE_NAME]:
            self.disable_run()
        else:
            self.enable_run()

    def get_valid_values(self):
        all_format = self.gui.pages[
            MANUAL_FORMAT_PAGE_NAME].get_data_format()
        valid_values = [(var['valid_low'], var['valid_high']) for var in
                        all_format]
        return valid_values

    def run_button_click(self):
        self.output_path = self.gui.run_button_click()
        if self.output_path:
            if self.matrix_input:
                self.run_matrix_fss()
            else:
                self.run_fss()

    @error_handler
    def run_matrix_fss(self):
        labels = []
        # remove the labels that are default
        for i, label in enumerate(self.gui.pages[
                                      DATA_PAGE_NAME].get_visible_labels()):
            if label == f"var{i + 1}":
                labels.append("")
            else:
                labels.append(label)
        variables_labels = [{'index': i + 1, 'label': label} for i, label in
                            enumerate(labels)]
        create_matrix_running_files(
            job_name=os.path.basename(self.output_path.split(".")[0]),
            nfacet=self.facets_num,
            variables_labels=variables_labels,
            correlation_type=self.gui.pages[
            DIMENSIONS_PAGE_NAME].get_correlation_type(),
            data_matrix=None,
            min_dim=self.min_dim, max_dim=self.max_dim,
            facet_details=self.facet_details,
            facet_var_details=self.facet_var_details,
            hypotheses_details=self.gui.pages[
            HYPOTHESIS_PAGE_NAME].get_hypotheses(),
            facet_dim_details=self.facet_dim_details,
            valid_values_range=None
        )


    @error_handler
    def run_fss(self):
        # get parameters for fss
        corr_type = self.gui.pages[
            DIMENSIONS_PAGE_NAME].get_correlation_type()
        data = self.gui.pages[DATA_PAGE_NAME].get_all_visible_data()
        labels = []
        # remove the labels that are default
        for i, label in enumerate(self.gui.pages[
                                      DATA_PAGE_NAME].get_visible_labels()):
            if label == f"var{i + 1}":
                labels.append("")
            else:
                labels.append(label)
        variables_labels = [{'index': i + 1, 'label': label} for i, label in
                            enumerate(labels)]
        self.facet_var_details = self.gui.pages[
            FACET_VAR_PAGE_NAME].get_all_var_facets_indices()
        self.facet_dim_details = self.gui.pages[
            FACET_DIM_PAGE_NAME].get_facets_dim()
        hypotheses_details = self.gui.pages[
            HYPOTHESIS_PAGE_NAME].get_hypotheses()

        valid_values_range = self.get_valid_values()
        create_running_files(
            job_name=os.path.basename(self.output_path.split(".")[0]),
            nfacet=self.facets_num,
            variables_labels=variables_labels,
            correlation_type=corr_type,
            data_matrix=data,
            min_dim=self.min_dim, max_dim=self.max_dim,
            facet_details=self.facet_details,
            facet_var_details=self.facet_var_details,
            hypotheses_details=hypotheses_details,
            facet_dim_details=self.facet_dim_details,
            valid_values_range=valid_values_range
        )
        try:
            run_fortran(corr_type, self.output_path)
        except Exception as e:
            raise e
        else:
            self.enable_view_results()
            self.gui.show_msg("Finished running FSS Successfully.\n"
                              'Click on "Open" to view results',
                              title="Job Finished Successfully",
                              buttons=["Open:primary", "Close:secondary"],
                              yes_commend=self.open_results)

    def load_data_page(self):
        # load data
        self.data_file_path = self.gui.pages[
            INPUT_PAGE_NAME].get_data_file_path()
        self.lines_per_var = self.gui.pages[
            INPUT_PAGE_NAME].get_lines_per_var()
        if self.data_file_path:
            self.enable_view_input()
        #
        if self.manual_input:
            data_format = self.gui.pages[
                MANUAL_FORMAT_PAGE_NAME].get_data_format()
            data = load_recordad_data(self.data_file_path,
                                      lines_per_var=self.lines_per_var,
                                      manual_format=data_format)
            data.columns = [row["label"] for row in data_format]
        else:
            if not self.data_file_path:
                data = get_random_data()
            else:
                delimiter = self.gui.pages[INPUT_PAGE_NAME].get_delimiter()
                try:
                    data = load_recordad_data(self.data_file_path,
                                              lines_per_var=self.lines_per_var,
                                              delimiter=delimiter)
                except Exception as e:
                    if IS_PRODUCTION():
                        raise DataLoadingException(e)
                    else:
                        raise e
            data.columns = [f"var{i + 1}" for i in
                            range(len(data.columns))]
        ##########
        self.gui.pages[DATA_PAGE_NAME].show_data(data)

    def load_facet_var_page(self):
        facets_details = self.gui.pages[FACET_PAGE_NAME].get_facets_details()
        self.get_labels()
        self.gui.pages[FACET_VAR_PAGE_NAME].create_facet_variable_table(
            var_labels=self.var_labels,
            facet_details=facets_details, )

    def get_labels(self):
        if self.matrix_input:
            self.var_labels = self.gui.pages[MANUAL_FORMAT_PAGE_NAME].get_labels()
        else:
            self.var_labels = self.gui.pages[DATA_PAGE_NAME].get_visible_labels()

    def load_facet_dim_page(self):
        max_dim = max(self.gui.pages[DIMENSIONS_PAGE_NAME].get_dimensions())
        min_dim = min(self.gui.pages[DIMENSIONS_PAGE_NAME].get_dimensions())
        self.gui.pages[FACET_DIM_PAGE_NAME].create_facet_dimension_table(
            max_dim=max_dim,
            min_dim=min_dim,
            num_facets=len(
                self.gui.pages[FACET_PAGE_NAME].get_facets_details()))

    @error_handler
    def run_process(self):
        self.gui.run_process()

    def load_matrix_file(self):
        self.gui.pages[MATRIX_INPUT_PAGE_NAME].browse_file()
        data_file_path = self.gui.pages[
            MATRIX_INPUT_PAGE_NAME].entry_data_file.get()
        if self.data_file_path != data_file_path:
            self.init_controller_attributes()
            self.data_file_path = data_file_path

    @error_handler
    def load_recorded_data_file(self):
        def suggest_delimiter(path):
            file_extension = os.path.splitext(path)[
                1].lower()
            if file_extension in ['.csv', '.xlsx', '.xls']:
                self.gui.pages[INPUT_PAGE_NAME].set_delimiter("Comma")
            elif file_extension == '.tsv':
                self.gui.pages[INPUT_PAGE_NAME].set_delimiter('Tab')
            else:
                self.gui.pages[INPUT_PAGE_NAME].set_delimiter(DELIMITER_1_D,
                                                              readonly=False)

        self.gui.pages[INPUT_PAGE_NAME].browse_file()
        data_file_path = self.gui.pages[INPUT_PAGE_NAME].entry_data_file.get()
        if self.data_file_path != data_file_path:
            self.init_controller_attributes()
            self.data_file_path = data_file_path
        if self.data_file_path:
            self.gui.pages[INPUT_PAGE_NAME].default_entry_lines()
            suggest_delimiter(self.data_file_path)

    @error_handler
    def save_data(self):
        file_name = self.gui.save_file(file_types=[('csv', '*.csv')],
                                       default_extension=".csv", )
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
        self.navigator.show_page(MANUAL_FORMAT_PAGE_NAME)
        self.navigate_page(MANUAL_FORMAT_PAGE_NAME)

    def load_hypothesis_page(self):
        self.gui.pages[HYPOTHESIS_PAGE_NAME].create_entries(self.facets_num)

    def show_help(self, section=None):
        if not section:
            section = help_pages_dict[self.navigator.get_current()]
        self.gui.show_help_windw(section)

    def show_diagram_window(self, dim, facet):
        from lib.fss.fss_output_parser import parse_output
        self.get_labels()
        output = parse_output(self.output_path)
        graph_data_list = []
        axes = list(range(dim))
        axes_pairs = [(a, b) for idx, a in enumerate(axes) for b in
                      axes[idx + 1:]]
        for a, b in axes_pairs:
            coors = output["dimensions"][dim]["coordinates"]
            x = [point['coordinates'][a] for point in coors]
            y = [point['coordinates'][b] for point in coors]
            index = [point['serial_number'] for point in coors]
            labels = [self.var_labels[i - 1] for i in index]
            legend = [dict(index=index[i], value=labels[i]) for i in range(len(
                index))]
            graph = dict(
                x=x,
                y=y,
                annotations=index,
                title=f"FSS Solution d={dim} {a + 1}X{b + 1}",
                legend=legend
            )
            graph_data_list.append(graph)
            if facet is not None:
                index = [point['serial_number'] for point in coors]
                annotations = [self.facet_var_details[i - 1][
                                   facet - 1] for i in index]
                legend = [
                    dict(index=i + 1, value=self.facet_details[facet - 1][i])
                    for i in range(len(self.facet_details[facet - 1]))]
                graph = dict(
                    x=x,
                    y=y,
                    annotations=annotations,
                    title=f"Facet {chr(64 + facet)}: d={dim} {a + 1}X{b + 1}",
                    legend=legend,
                )
                if dim == 2:
                    for model in output["models"]:
                        if model["facet"] != facet: continue
                        m_graph = dict(x=x,
                                       y=y,
                                       annotations=annotations,
                                       title=f"Facet {chr(64 + facet)}: d={dim} {a + 1}X{b + 1}",
                                       legend=legend)
                        m_graph["geoms"] = ShapeFactory.shapes_from_list(model[
                                                                             "divide_geoms"])
                        m_graph["caption"] = f"Separation index for" \
                                             f" {model['deviant_points_num']} Deviant " \
                                             f"Points Is  {model['seperation_index']}"
                        graph_data_list.append(m_graph)
                else:
                    graph_data_list.append(graph)
        self.gui.show_diagram_window(graph_data_list)
        self.gui.diagram_window.bind("<F1>", lambda e: self.show_help(
            "facet_diagrams_screen"))


class Validator():
    def __init__(self, gui):
        self.gui = gui

    def mode_dependent(func):
        def wrapper(*args, **kwargs):
            if IS_NO_VALIDATE():
                return
            else:
                return func(*args, **kwargs)

        return wrapper

    @staticmethod
    @mode_dependent
    def validate_input_page(data_path):
        if not data_path:
            raise FileNotFoundError("Please chose a data file for the "
                                    "analysis.")
        if not os.path.isfile(data_path):
            raise FileNotFoundError(f"Data File not found: {data_path}.")

    @staticmethod
    @mode_dependent
    def validate_manual_input(manual_input):
        if not manual_input or len(manual_input) < 3:
            raise Exception(
                "Usage Error:\nAt least three variable must be"
                " inserted in order for the fssa to run.")

    @staticmethod
    @mode_dependent
    def validate_data_page(data, labels):
        if len(labels) < 3:
            raise Exception(
                "Usage Error:\nAt least three variable must be"
                " inserted in order for the fssa to run.")
        for label in labels:
            if not label.isascii():
                raise Exception(
                    "Usage Error:\nAll variable labels must be entirely "
                    "ASCII characters and"
                    f' "{label}" contains non-ASCII characters.')

    @staticmethod
    @mode_dependent
    def validate_facet_var_page(facet_var):
        ## eg. facet_var: [[0,1,0,0],[1,7,1,2],[1,7,1,2], etc..]
        ## where 0 us undefined
        pass


class Navigator():
    class Page():
        def __init__(self, name, show=True):
            self.name: str = name
            self.show: bool = show

    def __init__(self, pages_list=None):
        self.pages_list = [Navigator.Page(page_name) for page_name in
                           pages_list]
        self.index: int = 0

    def append_page(self, page_name):
        self.pages_list.append(page_name)

    def pop_page(self, index=None):
        return self.pages_list.pop(index)

    ######
    def set_page(self, page_name: str):
        self.index = self.get_index(page_name)

    ######

    def get_next(self) -> str:
        if self.index == len(self.pages_list):
            return None
        for i in range(self.index + 1, len(self.pages_list)):
            if self.pages_list[i].show:
                return self.pages_list[i].name

    def get_current(self) -> str:
        for i in range(self.index, len(self.pages_list)):
            if self.pages_list[i].show:
                return self.pages_list[i].name

    def get_prev(self) -> str:
        if self.index == 0:
            return None
        for i in range(self.index - 1, -1, -1):
            if self.pages_list[i].show:
                return self.pages_list[i].name

    ######

    def hide_page(self, name: str):
        index = self.find(name)
        if index is None:
            raise Exception(
                "Usage Error:\nCan't hide page that doesn't exist")
        self.pages_list[index].show = False

    def show_page(self, name: str):
        index = self.find(name)
        if index is None:
            raise Exception(
                "Usage Error:\nCan't show page that doesn't exist")
        self.pages_list[index].show = True

    def add_block(self, name: str):
        index = self.get_index(name)
        for i in range(index + 1, len(self.pages_list)):
            self.pages_list[i].show = False

    def remove_block(self, name: str):
        index = self.get_index(name)
        for i in range(index + 1, len(self.pages_list)):
            self.pages_list[i].show = True

    ######
    def get_index(self, name):
        for i, page in enumerate(self.pages_list):
            if page.name == name:
                return i
        raise Exception(
            "Usage Error:\n Can't get index of page that doesn't exist")

    def find(self, name):
        for i, page in enumerate(self.pages_list):
            if page.name == name:
                return i


if __name__ == '__main__':
    controller = Controller()
    controller.run_process()
