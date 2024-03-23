from lib.fss.recoding import needs_recoding
from lib.utils import *


def invalid_fields(data):
    res = dict(
        passed=True,
        row_num=None,
    )
    for i, row in enumerate(data):
        for entry in row:
            try:
                if entry.strip() != "":
                    if int(entry) != eval(entry):
                        res['passed'] = True
                        res['row_num'] = i
                        return res
            except ValueError:
                # This is the case when the entry can't be converted to int
                res['passed'] = True
                res['row_num'] = i
                return res
            except SyntaxError:
                # This is the case when the entry has a starting zero
                # e.g 01, 02, 03, etc...
                res['passed'] = True
                res['row_num'] = i
                return res
    return res


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
        res = invalid_fields(data)
        if not res["passed"]:
            raise Exception(
                f"Usage Error Row {res['row_num']}:\nThe data fields must "
                f"be "
                f"numeric "
                "and in the "
                "range of 0-99.")
        res = needs_recoding(data)
        if needs_recoding(data):
            raise Exception(
                f"Usage Error Row {res['row_num']}:\nRecorded data values "
                "must be between 1-99."
                " You can use the recoding option to recode the data to "
                "this values range.")
        if len(labels) < 3:
            raise Exception(
                f"Usage Error:\nAt least three variable must be"
                " inserted in order for the fssa to run.")
        for i, label in enumerate(labels):
            if not label.isascii():
                raise Exception(
                    f"Usage Error :\nAll variable labels must be entirely "
                    "ASCII characters and"
                    f' label {i} : "{label}" contains non-ASCII characters.')

    @staticmethod
    @mode_dependent
    def validate_facet_var_page(facet_var):
        ## eg. facet_var: [[0,1,0,0],[1,7,1,2],[1,7,1,2], etc..]
        ## where 0 us undefined
        pass
