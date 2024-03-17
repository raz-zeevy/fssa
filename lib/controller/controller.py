# controller.py
import warnings
import pandas as pd
from lib.controller.graph_generator import generate_graphs
from lib.controller.navigator import Navigator
from lib.controller.validator import Validator
from lib.gui import GUI
from lib.fss.fss_module import load_recorded_data, \
    load_matrix_data, create_matrix_running_files, run_matrix_fortran
from lib.fss.fss_module import create_running_files, run_fortran
from lib.utils import *
import pynput.keyboard

SUPPORTED_RECORDED_DATA_FORMATS = ['.csv', '.xlsx', '.xls', 'tsv']


class Controller:
    def __init__(self):
        self.gui = GUI()
        self.bind_gui_events()
        self.keyboard = pynput.keyboard.Controller()
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

        # Override the default showwarning method with your custom one
        if IS_PRODUCTION():
            warnings.showwarning = self.custom_show_warning

    def custom_show_warning(self, message, category, filename, lineno,
                            file=None,
                            line=None):
        # Convert the warning message to a string and display it using your GUI
        warning_msg = f"{message}"
        # Assuming you have a GUI instance available as `self.gui`
        self.gui.show_warning("Warning", warning_msg)

    def reset_session(self):
        pass

    def init_controller_attributes(self):
        self.delimiter = None
        self.data_file_path = None
        self.data_file_extension = None
        self.var_labels = None
        self.has_header = False
        self.locality_weight = [2]
        self.facet_var_details = []
        self.facet_details = []
        self.facet_dim_details = {}
        #
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].create_data_table()
        self.gui.pages[INPUT_PAGE_NAME].reset_entries()

    def init_navigator(self):
        navigator = Navigator(self.gui)
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

    ######################
    # App Infrastructure #
    ######################

    def shutdown(self):
        # Perform any cleanup necessary before closing the application
        if self.gui:
            # Assuming your GUI class has a root Tkinter window
            self.gui.root.destroy()  # This will close the Tkinter window without exiting Python

    ##############
    #  Bindings  #
    ##############

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
        # data page
        self.gui.pages[DATA_PAGE_NAME]. \
            button_save.bind("<Button-1>",
                             lambda x: self.save_data())
        self.gui.pages[DATA_PAGE_NAME]. \
            button_reload.configure(command=self.load_data_page)
        self.gui.pages[DATA_PAGE_NAME].button_recode.config(
            command=lambda: self.gui.show_recode_window()
        )
        # Facet Page
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
        self.gui.file_menu.entryconfig("Exit", command=self.shutdown)
        ### Input Menu
        if not self.matrix_input:
            self.gui.input_data_menu.entryconfig("Data",
                                                 command=lambda: self.slide_to_page(
                                                     DATA_PAGE_NAME))
        self.gui.input_data_menu.entryconfig("Variables",
                                             command=lambda: self.slide_to_page(
                                                 MANUAL_FORMAT_PAGE_NAME))
        ### FSSA Menu
        self.gui.FSSA_menu.entryconfig("Dimensions & Coeffs",
                                       command=lambda: self.slide_to_page(
                                           DIMENSIONS_PAGE_NAME))
        self.gui.FSSA_menu.entryconfig("Technical Options",
                                       command=lambda:
                                       self.gui.show_technical_options_window(
                                           self.locality_weight))
        self.gui.facet_menu.entryconfig("Element Labels",
                                        command=lambda: self.slide_to_page(
                                            FACET_PAGE_NAME))
        self.gui.facet_menu.entryconfig("Variable Elements",
                                        command=lambda: self.slide_to_page(
                                            FACET_VAR_PAGE_NAME))
        self.gui.facet_menu.entryconfig("Hypotheses",
                                        command=lambda: self.slide_to_page(
                                            HYPOTHESIS_PAGE_NAME))
        self.gui.facet_menu.entryconfig("Diagrams",
                                        command=lambda: self.slide_to_page(
                                            FACET_DIM_PAGE_NAME))
        ### View Menu
        self.gui.view_menu.entryconfig("Next", command=self.next_page)
        self.gui.view_menu.entryconfig("Previous", command=self.previous_page)
        ### Help Menu
        self.gui.help_menu.entryconfig("Contents",
                                       command=lambda: self.show_help())
        self.gui.help_menu.entryconfig("Help on current screen",
                                       command=lambda: self.keyboard.press(
                                           pynput.keyboard.Key.f1))
        self.gui.help_menu.entryconfig("Open Readme.txt", command=lambda:
        os.startfile(os.path.join(get_path("readme.txt"))))
        self.gui.help_menu.entryconfig("About", command=lambda:
        self.show_help("what_is_fssa"))
        #### Diamgrams Menu
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

    def bind_icons_menu(self):
        self.gui.m_button_help.config(command=lambda: self.keyboard.press(
                                           pynput.keyboard.Key.f1))
        self.gui.m_button_next.config(command=self.next_page)
        self.gui.m_button_prev.config(command=self.previous_page)

    def start_fss(self, matrix=False):
        self.navigator.pop_page(0)
        self.gui.start_fss()
        if matrix:
            self.matrix_input = True
            self.navigator.hide_page(INPUT_PAGE_NAME)
            self.navigator.hide_page(DATA_PAGE_NAME)
            self.navigator.show_page(MANUAL_FORMAT_PAGE_NAME)
            self.gui.set_menu_matrix_data()
        else:
            self.navigator.hide_page(MATRIX_INPUT_PAGE_NAME)
            self.gui.set_menu_recorded_data()
        self.bind_menu()
        self.bind_keys()
        self.bind_icons_menu()
        # bind the navigation buttons
        self.gui.button_run.config(command=lambda: self.run_button_click())
        self.gui.button_next.config(command=self.next_page)
        self.gui.button_previous.config(command=self.previous_page)
        # start
        self.navigate_page(self.navigator.get_current())

    ###########################
    # Controls and Navigation #
    ###########################

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

    def previous_page(self):
        previous_page = self.navigator.get_prev()
        self.navigate_page(previous_page)

    def update_navigation_buttons(self):
        # change the state of previous and next buttons
        if self.navigator.get_prev():
            self.gui.option_previous_config(state="normal")
            self.gui.view_menu.entryconfig('Previous',
                                           state="normal")
        else:
            self.gui.option_previous_config(state="disabled")
            self.gui.view_menu.entryconfig('Previous',
                                           state="disabled")
        if self.navigator.get_next():
            self.gui.option_next_config(state="normal")
            self.gui.view_menu.entryconfig('Next',
                                           state="normal")
        else:
            self.gui.option_next_config(state="disabled")
            self.gui.view_menu.entryconfig('Next',
                                           state="disabled")

    def navigate_page(self, page_name: str):
        # switch page on gui
        self.gui.switch_page(page_name)
        self.navigator.set_page(page_name)

        # change the state of previous and next buttons
        self.update_navigation_buttons()

        # change the state of the run button
        if page_name in [INPUT_PAGE_NAME, MATRIX_INPUT_PAGE_NAME,
                         MANUAL_FORMAT_PAGE_NAME,
                         DATA_PAGE_NAME, DIMENSIONS_PAGE_NAME]:
            self.gui.option_run_config(state="disabled")
        else:
            self.gui.option_run_config(state="normal")

    def slide_to_page(self, page_name: str):
        while self.navigator.get_index(page_name) > self.navigator.get_index(
                self.navigator.get_current()):
            if not self.next_page(): return
        while self.navigator.get_index(page_name) < self.navigator.get_index(
                self.navigator.get_current()):
            self.previous_page()

    @error_handler
    def next_page(self) -> bool:
        """ Navigate to the next page and returns True if successful."""
        cur_page = self.navigator.get_current()
        next_page = self.navigator.get_next()
        # Input Page
        if cur_page == INPUT_PAGE_NAME:
            self.manual_input = self.gui.pages[
                INPUT_PAGE_NAME].is_manual_input()
            Validator.validate_input_page(
                data_path=self.gui.pages[
                    INPUT_PAGE_NAME].get_data_file_path(),
                lines_num=self.gui.pages[
                    INPUT_PAGE_NAME].get_lines_per_var(),
                is_manual_input=self.manual_input,
                additional_options=self.gui.pages[
                    INPUT_PAGE_NAME].additional_options)
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
            self.gui.pages[DIMENSIONS_PAGE_NAME].set_number_of_variables(
                len(self.gui.pages[DATA_PAGE_NAME].get_visible_labels()))
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

        if self.navigator.get_next() == DATA_PAGE_NAME:
            self.load_data_page()
        self.navigate_page(self.navigator.get_next())
        return True

    #################
    #  Gui Methods  #
    #################

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
        self.navigator.update_menu()

    def run_button_click(self):
        self.output_path = self.gui.run_button_dialogue()
        if self.output_path:
            if self.matrix_input:
                self.run_matrix_fss()
            else:
                self.run_fss()

    def load_data_page(self):
        # load data
        self.data_file_path = self.gui.pages[
            INPUT_PAGE_NAME].get_data_file_path()
        self.lines_per_var = self.gui.pages[
            INPUT_PAGE_NAME].get_lines_per_var()
        self.delimiter = self.gui.pages[
            INPUT_PAGE_NAME].get_auto_parsing_format()
        #
        if self.data_file_path:
            self.enable_view_input()
        #
        if self.manual_input:
            data_format = self.gui.pages[
                MANUAL_FORMAT_PAGE_NAME].get_data_format()
            data = load_recorded_data(self.data_file_path,
                                      lines_per_var=self.lines_per_var,
                                      manual_format=data_format,
                                      extension=self.data_file_extension,
                                      has_header=self.has_header)
            data.columns = [row["label"] for row in data_format]
        else:
            try:
                data = load_recorded_data(self.data_file_path,
                                          lines_per_var=self.lines_per_var,
                                          delimiter=self.delimiter,
                                          extension=self.data_file_extension,
                                          has_header=self.has_header)
            except Exception as e:
                if IS_PRODUCTION():
                    raise DataLoadingException(e)
                else:
                    raise e
        ##########
        self.gui.pages[DATA_PAGE_NAME].show_data(data)

    def load_facet_var_page(self):
        facets_details = self.gui.pages[FACET_PAGE_NAME].get_facets_details()
        self.get_labels()
        self.gui.pages[FACET_VAR_PAGE_NAME].create_facet_variable_table(
            var_labels=self.var_labels,
            facet_details=facets_details, )

    def set_header(self, is_header):
        self.has_header = is_header

    def get_labels(self):
        if self.matrix_input:
            self.var_labels = self.gui.pages[
                MANUAL_FORMAT_PAGE_NAME].get_labels()
        else:
            self.var_labels = self.gui.pages[
                DATA_PAGE_NAME].get_visible_labels()

    def load_facet_dim_page(self):
        max_dim = max(self.gui.pages[DIMENSIONS_PAGE_NAME].get_dimensions())
        min_dim = min(self.gui.pages[DIMENSIONS_PAGE_NAME].get_dimensions())
        self.gui.pages[FACET_DIM_PAGE_NAME].create_facet_dimension_table(
            max_dim=max_dim,
            min_dim=min_dim,
            num_facets=len(
                self.gui.pages[FACET_PAGE_NAME].get_facets_details()))

    def switch_to_manual_format_page(self):
        self.manual_input = True
        self.navigator.show_page(MANUAL_FORMAT_PAGE_NAME)
        self.navigate_page(MANUAL_FORMAT_PAGE_NAME)

    def load_hypothesis_page(self):
        self.gui.pages[HYPOTHESIS_PAGE_NAME].create_entries(self.facets_num)

    ################
    # FSSA Methods #
    ################

    def load_matrix(self):
        self.data_file_path = self.gui.pages[
            MATRIX_INPUT_PAGE_NAME].get_data_file_path()
        Validator.validate_matrix_input_page(self.data_file_path)
        matrix_details = self.gui.pages[MATRIX_INPUT_PAGE_NAME]. \
            get_matrix_details()
        try:
            self.matrix = load_matrix_data(self.data_file_path,
                                           matrix_details)
        except:
            raise DataLoadingException("Error loading matrix data")
        manual_input = self.gui.pages[MANUAL_FORMAT_PAGE_NAME]
        # reset existing variables
        if manual_input.data_table:
            manual_input.create_data_table()
        # insert new variables
        for _ in range(len(self.matrix)):
            manual_input.add_variable("", "", "", "", "")
        manual_input.set_matrix_edit_mode()
        self.gui.pages[DIMENSIONS_PAGE_NAME].set_matrix_mode()

    @error_handler
    def run_matrix_fss(self):
        labels = []
        # remove the labels that are default
        all_labels = self.gui.pages[MANUAL_FORMAT_PAGE_NAME].get_labels()
        for i, label in enumerate(all_labels):
            if label == f"var{i + 1}":
                labels.append("")
            else:
                labels.append(label)
        variables_labels = [{'index': i + 1, 'label': label} for i, label in
                            enumerate(labels)]
        create_matrix_running_files(
            job_name=os.path.basename(self.output_path.split(".")[0]),
            matrix_details=self.gui.pages[
                MATRIX_INPUT_PAGE_NAME].get_matrix_details(),
            iweigh=self.locality_weight[0],
            matrix_path=self.data_file_path,
            correlation_type=self.gui.pages[
                DIMENSIONS_PAGE_NAME].get_correlation_type(),
            min_dim=self.min_dim, max_dim=self.max_dim,
            nfacet=self.facets_num,
            variables_labels=variables_labels,
            facet_details=self.facet_details,
            facet_var_details=self.facet_var_details,
            hypotheses_details=self.gui.pages[
                HYPOTHESIS_PAGE_NAME].get_hypotheses(),
            facet_dim_details=self.facet_dim_details)
        try:
            run_matrix_fortran(self.output_path)
        except Exception as e:
            raise e
        else:
            self.enable_view_results()
            self.gui.show_msg("Finished running FSS Successfully.\n"
                              'Click on "Open" to view results',
                              title="Job Finished Successfully",
                              buttons=["Open:primary", "Close:secondary"],
                              yes_commend=self.open_results)

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

        valid_values_range = self.gui.pages[
            MANUAL_FORMAT_PAGE_NAME].get_vars_valid_values()
        create_running_files(
            job_name=os.path.basename(self.output_path.split(".")[0]),
            nfacet=self.facets_num,
            variables_labels=variables_labels,
            iweigh=self.locality_weight[0],
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
        def suggest_parsing(path):
            file_extension = os.path.splitext(path)[
                1].lower()
            if file_extension in SUPPORTED_RECORDED_DATA_FORMATS:
                self.data_file_extension = file_extension
                self.gui.pages[INPUT_PAGE_NAME].disable_additional_options()
                self.gui.pages[INPUT_PAGE_NAME].automatic_parsable = True
                # Ask the user whether to treat the first row as a header
                self.gui.show_msg(
                    "Do you want to treat the first row as a header?",
                    title="Header",
                    buttons=["Yes:primary", "No:primary"],
                    yes_commend=lambda: self.set_header(True),
                    no_commend=lambda: self.set_header(False))
            else:
                self.gui.pages[INPUT_PAGE_NAME].enable_additional_options()
                self.gui.pages[INPUT_PAGE_NAME].automatic_parsable = False

        self.gui.pages[INPUT_PAGE_NAME].browse_file()
        data_file_path = self.gui.pages[INPUT_PAGE_NAME].entry_data_file.get()
        if self.data_file_path != data_file_path:
            self.init_controller_attributes()
            self.data_file_path = data_file_path
        if self.data_file_path:
            self.gui.pages[INPUT_PAGE_NAME].default_entry_lines()
            suggest_parsing(self.data_file_path)

    @error_handler
    def save_data(self):
        file_name = self.gui.save_file_diaglogue(file_types=[('csv', '*.csv')],
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

    ####################
    # External Windows #
    ####################

    def show_help(self, section=None):
        if not section:
            section = help_pages_dict[self.navigator.get_current()]
        self.gui.show_help_windw(section)

    def show_diagram_window(self, dim, facet):
        graph_data_list = generate_graphs(self, dim, facet)
        self.gui.show_diagram_window(graph_data_list)
        self.gui.diagram_window.bind("<F1>",
                                     lambda e: controller.show_help(
                                         "facet_diagrams_screen"))


if __name__ == '__main__':
    controller = Controller()
    # controller.gui.pages[START_PAGE_NAME].button_matrix_data.invoke()
    controller.gui.pages[START_PAGE_NAME].button_recorded_data.invoke()
    controller.run_process()
