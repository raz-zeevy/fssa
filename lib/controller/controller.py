# controller.py
import os.path
import subprocess
import warnings
import pandas as pd
from typing import List
from lib.controller.sessions_history import SessionsHistory
from lib.controller.graph_generator import generate_graphs
from lib.controller.navigator import Navigator
from lib.controller.session import Session
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
        self.history = SessionsHistory(callback=self.update_history)
        ###
        self.init_controller_attributes()
        self.active_variables_details = []
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

        self.gui.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Override the default showwarning method with your custom one
        if IS_PRODUCTION():
            warnings.showwarning = self.custom_show_warning
    def on_close(self):
        # Prompt the user with a message box
        if IS_PRODUCTION():
            result = self.gui.show_msg(
                "Do you want to save the current session before exiting?",
                title="Exit",
                yes_command=self.save_session_click,
                buttons=["Yes:primary", "No:secondary", "Cancel:secondary"]
            )
            if result == "Yes":
                self.save_session_click()
                self.gui.root.destroy()  # Close the application after saving
            elif result == "No":
                self.gui.root.destroy()  # Close the application without saving
            else:
                pass  # Do nothing (cancel the close operation)
        else:
            self.gui.root.destroy()
    def custom_show_warning(self, message, category, filename, lineno,
                            file=None,
                            line=None):
        # Convert the warning message to a string and display it using your GUI
        warning_msg = f"{message}"
        # Assuming you have a GUI instance available as `self.gui`
        self.gui.show_warning("Warning", warning_msg)

    def init_controller_attributes(self):
        self.active_variables_details = []
        self.update_save_path("")
        self.delimiter = None
        self.data = None
        self.org_data = None
        self.data_file_path = None
        self.save_path = None
        self.data_file_extension = None
        self.var_labels = None
        self.has_header = False
        self.locality_weight = [2]
        self.facet_var_details = []
        self.facet_details = []
        self.facet_dim_details = {}
        #
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].create_data_table()
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].unset_limited_edit_mode()
        self.gui.pages[INPUT_PAGE_NAME].reset_entries()
        self.gui.pages[DIMENSIONS_PAGE_NAME].set_default()

    def init_navigator(self):
        navigator = Navigator(self.gui)
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
                                            "options you selected and the "
                                            "current formatting. "
                                            "Alternatively if you use "
                                            ".csv/.xls "
                                            "that "
                                            "has already been loaded, "
                                            "start a new session and reload "
                                            "the data file.")
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

    #############
    # User Flow #
    #############
    def reset_session(self, matrix):
        while self.navigator.get_prev():
            self.previous_page()
        self.init_controller_attributes()
        self.on_facet_num_change(None)
        if matrix:
            self.navigator.show_page(MATRIX_INPUT_PAGE_NAME)
            self.navigator.hide_page(INPUT_PAGE_NAME)
            self.gui.switch_page(MATRIX_INPUT_PAGE_NAME)
            self.matrix_input = True
            self.navigator.hide_page(DATA_PAGE_NAME)
            self.gui.set_menu_matrix_data()
        else:
            self.navigator.hide_page(MATRIX_INPUT_PAGE_NAME)
            self.navigator.show_page(INPUT_PAGE_NAME)
            self.gui.switch_page(INPUT_PAGE_NAME)
            self.matrix_input = False
            self.navigator.show_page(DATA_PAGE_NAME)
            self.gui.set_menu_recorded_data()

    def open_session(self):
        self.reset_session()

    def save_session(self, path):
        session = Session(self)
        self.history.add(path)
        session.save(path)


    def load_session(self, path):
        self.history.add(path)
        session = Session(path=path)
        session.load_to_controller(self)

    def start_fss(self, matrix=False):
        self.navigator.pop_page(0)
        self.gui.start_fss()
        self.update_history()
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

    ##############
    #  Bindings  #
    ##############

    def bind_keys(self):
        self.gui.root.bind("<F1>", lambda x: self.show_help())
        self.gui.root.bind("<Control-n>", lambda x: self.new_session_click())
        self.gui.root.bind("<Control-o>", lambda x: self.open_session_click())
        self.gui.root.bind("<Control-s>", lambda x: self.save_session_click())

    def bind_gui_events(self):
        # Matrix page
        self.gui.pages[MATRIX_INPUT_PAGE_NAME]. \
            button_browse.bind("<Button-1>",
                               lambda x: self.load_matrix_file())
        # input page
        self.gui.pages[INPUT_PAGE_NAME]. \
            button_browse.bind("<Button-1>",
                               lambda x: self.browse_recorded_data_file())
        self.gui.pages[INPUT_PAGE_NAME]. \
            button_load.bind("<Button-1>",
                               lambda x: self.load_recorded_data_file())
        # Manual Page:
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME]. \
            update_variables = self.reload_variables
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].button_reload.configure(
            command=self.load_csv_init
        )
        # data page
        self.gui.pages[DATA_PAGE_NAME]. \
            button_save.bind("<Button-1>",
                             lambda x: self.save_data())
        self.gui.pages[DATA_PAGE_NAME].button_recode.config(
            command=lambda: self.gui.show_recode_window()
        )
        self.gui.pages[DATA_PAGE_NAME].select_variables_subset = \
        self.update_facets_var_selection
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
        self.gui.file_menu.entryconfig("New", command=self.new_session_click)
        self.gui.file_menu.entryconfig("Save", command=self.save_session_click)
        self.gui.file_menu.entryconfig("Save As...",
                                       command=self.save_as_session_click)
        self.gui.file_menu.entryconfig("Open", command=self.open_session_click)
        self.gui.file_menu.entryconfig("Exit", command=self.shutdown)
        self.gui.input_data_menu.entryconfig("Recorded Data",
                                                command=lambda: self.new_session_click(
                                                    False))
        self.gui.input_data_menu.entryconfig("Coefficient Matrix",
                                                command=lambda: self.new_session_click(
                                                    True))
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
        self.gui.m_button_new.config(command=lambda : self.reset_session(
            matrix=self.matrix_input))
        self.gui.m_button_new.config(command=self.new_session_click)
        self.gui.m_button_save.config(command=self.save_session_click)
        self.gui.m_button_open.config(command=self.open_session_click)
        self.gui.m_button_next.config(command=self.next_page)
        self.gui.m_button_prev.config(command=self.previous_page)
        self.gui.m_button_run.config(command=self.run_button_click)

    ###########################
    # Controls and Navigation #
    ###########################

    def open_file(self, file, notepad=False, word=False):
        def open_file_in_notepad(file_path):
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File {file_path} does not exist")
            try:
                subprocess.run(['notepad', file_path], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to open file {file_path}: {e}")

        def open_file_in_word(file_path):
            try:
                subprocess.run(['start', 'winword', file_path], shell=True,
                               check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to open file {file_path}: {e}")
        if not notepad and not word:
            raise UserWarning("Please specify a program to open the file with")
        open_file = open_file_in_word if word else open_file_in_notepad
        open_file(file)

    def open_results(self):
        try:
            subprocess.run(['notepad', self.output_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to open file {self.output_path}: {e}")

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

    def disable_view_results(self):
        self.gui.view_menu.entryconfig("Output File", state="disabled")
        self.gui.view_menu.entryconfig("2D Diagram ", state="disabled")
        self.gui.view_menu.entryconfig("3D Diagram ", state="disabled")
        for menu in [self.gui.diagram_2d_menu, self.gui.diagram_3d_menu]:
            for i in range(self.facets_num):
                menu.entryconfig("Facet " + chr(65 + i), state="disabled")

    def enable_view_input(self):
        def view_input():
            self.data_file_path = self.gui.pages[
                INPUT_PAGE_NAME].get_data_file_path()
            if not self.data_file_path:
                raise FileNotFoundError("No input file was loaded")
            if not os.path.exists(self.data_file_path):
                raise FileNotFoundError(f"Can not find input file {self.data_file_path}")
            os.startfile(self.data_file_path)

        self.gui.view_menu.entryconfig("Input File", state="normal")
        self.gui.view_menu.entryconfig("Input File", command=view_input)

    def disable_view_input(self):
        self.gui.view_menu.entryconfig("Input File", state="disabled")

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
            self.gui.pages[MANUAL_FORMAT_PAGE_NAME].load_missing_values(
                self.are_missing_values)
        # Matrix Input page
        elif cur_page == MATRIX_INPUT_PAGE_NAME:
            self.load_matrix()
        # Manual Format Page
        elif cur_page == MANUAL_FORMAT_PAGE_NAME:
            # for recorded data
            if next_page == DATA_PAGE_NAME:
                Validator.validate_manual_input(self.gui.pages[
                                                    MANUAL_FORMAT_PAGE_NAME].get_data_format())
                self.manual_input = not self.gui.pages[
                    MANUAL_FORMAT_PAGE_NAME].limited_edit_mode
                if self.manual_input:
                    self.load_fixed_width()
                self.commit_data()
            # for matrix data
            elif next_page == DIMENSIONS_PAGE_NAME:
                self.gui.pages[DIMENSIONS_PAGE_NAME].set_number_of_variables(
                    self.gui.pages[MANUAL_FORMAT_PAGE_NAME]
                    .get_len_selected_vars())
        # Data Page
        elif cur_page == DATA_PAGE_NAME:
            Validator.validate_data_page(
                data=self.gui.pages[DATA_PAGE_NAME].get_all_visible_data(),
                labels=self.gui.pages[DATA_PAGE_NAME].get_visible_labels()
            )
            self.navigator.show_page(DIMENSIONS_PAGE_NAME)
            self.gui.pages[DIMENSIONS_PAGE_NAME].set_number_of_variables(
                len(self.gui.pages[DATA_PAGE_NAME].get_visible_labels()))
        # Dimension Page
        elif cur_page == DIMENSIONS_PAGE_NAME:
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
        elif cur_page == FACET_PAGE_NAME:
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
        elif cur_page == FACET_VAR_PAGE_NAME:
            Validator.validate_facet_var_page(self.gui.pages[
                                                  FACET_VAR_PAGE_NAME].get_all_var_facets_indices_values())
        self.navigate_page(self.navigator.get_next())
        return True

    #############
    # Save Load #
    # & New     #
    #############

    def save_session_click(self, save_path=None):
        if save_path:
            self.save_path = save_path
            self.update_save_path(save_path)
        if not self.save_path:
            self.save_as_session_click()
        else:
            self.save_session(self.save_path)

    def save_as_session_click(self):
        data_file_name = os.path.basename(self.gui.pages[
            INPUT_PAGE_NAME].get_data_file_path()).split(".")[0]
        save_path = self.gui.save_session_dialogue(data_file_name)
        if save_path:
            self.update_save_path(save_path)
            self.save_session(self.save_path)

    def update_save_path(self, path):
        self.save_path = path
        self.gui.set_save_title(self.save_path)

    def open_session_click(self):
        open_path = self.gui.open_session_dialogue()
        if open_path:
            self.load_session(open_path)

    def new_session_click(self, matrix=None):
        res = self.gui.show_msg("Do you want to save the "
                                              "current "
                                         "session before starting a new "
                                "one?", title="New Session",
                          yes_command=self.save_session_click,)
        if not res and not self.matrix_input:
            self.gui.set_menu_recorded_data()
        elif not res and self.matrix_input:
            self.gui.set_menu_matrix_data()
        if res in ['Yes', 'No']:
            if matrix is None: matrix = self.matrix_input
            self.reset_session(matrix=matrix)

    def load_data_page(self, data):
        print("Loading data")
        self.gui.pages[DATA_PAGE_NAME].show_data(data,
                                                 self.active_variables_details)

    def update_history(self):
        """
        this function gets at most 4 last sessions path's and updates
        the menu under file section with the paths and bind them with load_path
        :return:
        """
        paths = self.history.get_n(4)
        self.gui.update_history_menu(paths)

        # Bind each path to the corresponding menu item using its index
        menu_start_index = self.gui.file_menu.index('end') - len(
            paths) + 1  # Start index of the new paths
        for i, path in enumerate(paths):
            self.gui.file_menu.entryconfig(menu_start_index + i, command=lambda
                p=path: self.load_session(p))
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

    def update_facets_var_selection(self, selected_vars : list=None):
        # todo: remove this: update selection
        if selected_vars:
            for var in self.active_variables_details:
                var['show'] = False
            for i in selected_vars:
                self.active_variables_details[i]['show'] = True
        # update the current self.c_facet_var_details with the data
        # [{index: int, label : string,
        # facets : [int], show : bool}]
        facets_values = self.gui.pages[
            FACET_VAR_PAGE_NAME].get_all_var_facets_indices()
        for active_var in self.active_variables_details:
            if active_var['index'] in facets_values:
                active_var['facets'] = facets_values[active_var['index']]
        # rebuild facets
        print("reloading facets")
        self.gui.pages[FACET_VAR_PAGE_NAME].create_facet_variable_table(
            var_details=self.active_variables_details,
            facet_details=self.facet_details)
        # update with values
        facet_values = [var['facets'] for var in
                        self.active_variables_details if var['show']]
        self.gui.pages[FACET_VAR_PAGE_NAME].set_facets_vars(
            facet_values)

    def run_button_click(self):
        self.output_path = self.gui.run_button_dialogue()
        if self.output_path:
            if self.matrix_input:
                self.run_matrix_fss()
            else:
                self.run_fss()

    def reload_variables(self, selected_vars):
        self.select_csv_variables(selected_vars)

    def select_csv_variables(self, selected_vars_i):
        """
        scenraio: this function is called on "select vars." of the manual page
        :param selected_vars_i: the variables real-index (var_i) that
        matches the one in active_variables_data
        """
        # change the selection in active_variable_details
        for i, var in enumerate(self.active_variables_details):
            var['show'] = i in selected_vars_i
            var['remove'] = i not in selected_vars_i

    def load_csv(self):
        # init loading variables
        self.data_file_path = self.gui.pages[
            INPUT_PAGE_NAME].get_data_file_path()
        self.delimiter = self.gui.pages[
            INPUT_PAGE_NAME].get_auto_parsing_format()
        # load data
        try:
            data = load_recorded_data(self.data_file_path,
                                      lines_per_var=None,
                                      delimiter=self.delimiter,
                                      extension=self.data_file_extension,
                                      has_header=self.has_header)
        except Exception as e:
            if IS_PRODUCTION():
                raise DataLoadingException(e)
            else:
                raise e
        # saves the data to the controller, mostly for displaying it and
        # for later selection operations
        self.org_data = data
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].set_limited_edit_mode()

    def load_csv_init(self):
        """
        this function is called on "next" of the input page and
         - loads the entire csv into self.data
         - inits the manual page with variables
         - inits the active variables details []
        :return:
        """
        self.load_csv()
        # clear manual format (todo: for cases of reloading?)
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].clear_all_vars()
        # reset active variables details
        self.active_variables_details = []
        for i, var in enumerate(self.org_data.columns):
            # add to active_dat_details
            active_var = dict(label=var, index=i, facets=[],
                              show=True, remove=False)
            self.active_variables_details.append(active_var)
            # add to manual format with the real-index "var_i = i"
            self.gui.pages[MANUAL_FORMAT_PAGE_NAME].add_variable(
                label=var, var_i=i)
    def load_fixed_width(self):
        """
        Called on manual input when clicking "next" on "Manual Page"
        :return:
        """
        # init loading parameters
        self.data_file_path = self.gui.pages[
            INPUT_PAGE_NAME].get_data_file_path()
        self.lines_per_var = self.gui.pages[
            INPUT_PAGE_NAME].get_lines_per_var()
        data_format = self.gui.pages[
            MANUAL_FORMAT_PAGE_NAME].get_data_format()
        all_vars = self.gui.pages[
            MANUAL_FORMAT_PAGE_NAME].get_labels()
        # Load data
        data = load_recorded_data(self.data_file_path,
                                  lines_per_var=self.lines_per_var,
                                  manual_format=data_format,
                                  extension=self.data_file_extension,
                                  has_header=self.has_header)
        # Update active_variables_data with never seen variables
        for i, var in enumerate(all_vars):
            if i >= len(self.active_variables_details):
                # add to active_var_details
                active_var = dict(label=var, index=i, facets=[],
                                  show=True, remove=False)
                self.active_variables_details.append(active_var)
        while len(self.active_variables_details) > len(all_vars):
            self.active_variables_details.pop()
        self.org_data = data

    def commit_data(self):
        # Update toggled of variables
        manual_page = self.gui.pages[MANUAL_FORMAT_PAGE_NAME]
        selected_vars_i = manual_page.get_selected_var_indices()
        # these variables are used to iterate against active_var and labels
        # where because of selection they may be not at synch
        label_i = 0
        labels = manual_page.get_labels()
        for var in self.active_variables_details:
            # commit toggle
            var['show'] = var['index'] in selected_vars_i
            # commit labels
            if not var['remove']:
                var['label'] = labels[label_i]
                label_i += 1
        # Remove toggled off columns only on csv
        if not self.gui.pages[INPUT_PAGE_NAME].is_manual_input():
            # try:
            self.data = self.org_data.iloc[:, [i for i in selected_vars_i]]
            # except Exception:
            #     raise DataLoadingException("Error loading data."
         #                                "Are you sure the variables match the columns in the data file?")

        else:
            self.data = self.org_data
        # Commit labels to data
        self.data.columns = manual_page.get_selected_var_labels()
        # Show data on data page
        self.load_data_page(self.data)
        # Change the facets selection
        self.update_facets_var_selection(selected_vars_i)

    def load_facet_var_page(self):
        facets_details = self.gui.pages[FACET_PAGE_NAME].get_facets_details()
        self.gui.pages[FACET_VAR_PAGE_NAME].create_facet_variable_table(
            var_details=self.active_variables_details,
            facet_details=facets_details)

    def set_header(self, is_header):
        self.has_header = is_header

    def get_labels(self):
        if self.matrix_input:
            self.var_labels = self.gui.pages[
                MANUAL_FORMAT_PAGE_NAME].get_selected_var_labels()
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
        manual_input.set_limited_edit_mode()
        self.gui.pages[DIMENSIONS_PAGE_NAME].set_matrix_mode()

    def init_fss_attributes(self):
        # Input Page
        self.data_file_path = self.gui.pages[
            INPUT_PAGE_NAME].get_data_file_path()
        self.additional_options = self.gui.pages[
            INPUT_PAGE_NAME].additional_options
        self.fixed_width = self.gui.pages[INPUT_PAGE_NAME].get_fixed_width()
        self.lines_per_var = self.gui.pages[
            INPUT_PAGE_NAME].get_lines_per_var()
        # Dim Page
        self.correlation_type = self.gui.pages[
            DIMENSIONS_PAGE_NAME].get_correlation_type()
        self.iweigh = self.locality_weight[0]
        self.hypotheses_details = self.gui.pages[
            HYPOTHESIS_PAGE_NAME].get_hypotheses()
        self.facet_details = self.gui.pages[
            FACET_PAGE_NAME].get_facets_details()
        self.facet_var_details = self.gui.pages[
            FACET_VAR_PAGE_NAME].get_all_var_facets_indices_values()
        self.facet_dim_details = self.gui.pages[
            FACET_DIM_PAGE_NAME].get_facets_dim()
        # Manual Format Page
        if self.manual_input:
            self.manual_format_details = self.gui.pages[
                MANUAL_FORMAT_PAGE_NAME].get_data_format()
        if self.matrix_input:
            self.data_file_path = self.gui.pages[
                MATRIX_INPUT_PAGE_NAME].get_data_file_path()
            self.matrix_details = self.gui.pages[MATRIX_INPUT_PAGE_NAME]. \
                get_matrix_details()
        else:
            self.fss_data = self.gui.pages[
                DATA_PAGE_NAME].get_all_visible_data()
            self.valid_values_range = self.gui.pages[
                MANUAL_FORMAT_PAGE_NAME].get_vars_valid_values()
        self.fss_labels = []
        self.get_labels()
        if self.var_labels:
            for i, label in enumerate(self.var_labels):
                if label.strip() == f"var{i + 1}":
                    self.fss_labels.append("")
                else:
                    self.fss_labels.append(label)
            self.fss_var_labels = [{'index': i + 1, 'label': label} for i, label in
                                enumerate(self.fss_labels)]
        else:
            self.fss_labels = None
        facets_var_info = self.gui.pages[FACET_VAR_PAGE_NAME].get_all_var_facets_indices()
        for var in facets_var_info:
            self.active_variables_details[var]['facets'] = facets_var_info[
                var]

    @error_handler
    def run_matrix_fss(self):
        self.init_fss_attributes()
        create_matrix_running_files(
            job_name=os.path.basename(self.output_path.split(".")[0]),
            matrix_details=self.matrix_details,
            iweigh=self.locality_weight[0],
            matrix_path=self.data_file_path,
            correlation_type=self.correlation_type,
            min_dim=self.min_dim, max_dim=self.max_dim,
            nfacet=self.facets_num,
            variables_labels=self.fss_var_labels,
            facet_details=self.facet_details,
            facet_var_details=self.facet_var_details,
            hypotheses_details=self.hypotheses_details,
            facet_dim_details=self.facet_dim_details)
        try:
            run_matrix_fortran(self.output_path)
        except Exception as e:
            raise e
        else:
            self.enable_view_results()
            self.gui.show_msg("Finished running FSS Successfully.\n"
                              'Click on  "Close" > "View" > "2D\\3D Diagram" '
                              'to view '
                              "and to save the diagrams.\n"
                              'Click on "Open" to view results',
                              title="Job Finished Successfully",
                              buttons=["Open:primary", "Close:secondary"],
                              yes_command=self.open_results)

    @error_handler
    def run_fss(self):
        self.init_fss_attributes()
        create_running_files(
            job_name=os.path.basename(self.output_path.split(".")[0]),
            nfacet=self.facets_num,
            variables_labels=self.fss_var_labels,
            iweigh=self.locality_weight[0],
            correlation_type=self.correlation_type,
            data_matrix=self.fss_data,
            min_dim=self.min_dim, max_dim=self.max_dim,
            facet_details=self.facet_details,
            facet_var_details=self.facet_var_details,
            hypotheses_details=self.hypotheses_details,
            facet_dim_details=self.facet_dim_details,
            valid_values_range=self.valid_values_range
        )
        try:
            run_fortran(self.correlation_type, self.output_path)
        except Exception as e:
            self.disable_view_results()
            raise e
        else:
            self.enable_view_results()
            self.gui.show_msg("Finished running FSS Successfully.\n"
                              'Click on "Close" > "View" > "2D\\3D Diagram" '
                              'to view '
                              "and to save the diagrams.\n"
                              'Click on "Open" to view results',
                              title="Job Finished Successfully",
                              buttons=["Open:primary", "Close:secondary"],
                              yes_command=self.open_results)

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

    def _suggest_parsing(self, interactive=True):
        path = self.gui.pages[
            INPUT_PAGE_NAME].get_data_file_path()
        file_extension = os.path.splitext(path)[
            1].lower()
        if file_extension in SUPPORTED_RECORDED_DATA_FORMATS:
            if interactive:
                # Ask the user whether to treat the first row as a header
                res = self.gui.show_msg(
                    "Do you want to treat the first row as a header?",
                    title="Header",
                    buttons=["Yes:primary", "No:primary"],
                    yes_command=lambda: self.set_header(True),
                    no_command=lambda: self.set_header(False))
                if not res: return
            self.data_file_extension = file_extension
            self.gui.pages[INPUT_PAGE_NAME].disable_additional_options()
            self.gui.pages[INPUT_PAGE_NAME].automatic_parsable = True
        else:
            self.gui.pages[INPUT_PAGE_NAME].enable_additional_options()
            self.gui.pages[INPUT_PAGE_NAME].automatic_parsable = False
        self.enable_view_input()
    @error_handler
    def load_recorded_data_file(self):
        data_file_path = self.gui.pages[INPUT_PAGE_NAME].browse_file()
        if data_file_path:
            self.enable_view_input()
            self.gui.pages[INPUT_PAGE_NAME].default_entry_lines()
            self._suggest_parsing(interactive=True)
        if not self.gui.pages[
                INPUT_PAGE_NAME].is_manual_input():
            self.load_csv_init()

    def browse_recorded_data_file(self):
        data_file_path = self.gui.pages[INPUT_PAGE_NAME].browse_file()
        if data_file_path:
            self.enable_view_input()
        if not self.gui.pages[
            INPUT_PAGE_NAME].is_manual_input():
            self.load_csv()

    @error_handler
    def save_data(self):
        filename = f"" \
                   f"{os.path.basename(self.data_file_path).split('.')[0]}-" \
                   f"Active"
        file_name = self.gui.save_file_diaglogue(file_types=[('csv', '*.csv')],
                                                 default_extension=".csv",
                                                 initial_file_name=filename)
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
