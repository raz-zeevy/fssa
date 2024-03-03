from lib.fss.recoding import needs_recoding
from lib.utils import *


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
    def validate_input_page(data_path, lines_num, is_manual_input,
                            additional_options):
        if not data_path:
            raise FileNotFoundError("Please chose a data file for the "
                                    "analysis.")
        if additional_options and not lines_num:
            raise ValueError(f"You must state the lines per case in order to "
                             f"proceed.")
        if not os.path.isfile(data_path):
            raise FileNotFoundError(f"Data File not found: {data_path}.")

    @staticmethod
    @mode_dependent
    def validate_matrix_input_page(data_path):
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
        if needs_recoding(data):
            raise Exception(
                "Usage Error:\nRecorded data values must be between 1-99."
                " You can use the recoding option to recode the data to "
                "this values range.")
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