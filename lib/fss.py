# Python code to run the specified command using subprocess

import subprocess
import os
from typing import List, Dict
import numpy as np
import pandas as pd
from lib.utils import *
from lib.fss_parsers import *

ENTRY_WIDTH = 2

# Output Paths
SCRIPT_NESTING_PREFIX = "..\\..\\..\\"
p_OUTPUT_DIR = "output"
OUTPUT_MAT_FILE = "MONOASC.MAT"
OUTPUT_FILE_NAME = "DJK21.FSS"
p_OUTPUT_FILE = os.path.join(p_OUTPUT_DIR, OUTPUT_FILE_NAME)
p_OUTPUT_MAT_FILE = os.path.join(p_OUTPUT_DIR, OUTPUT_MAT_FILE)

# Input paths
RUN_FILES_DIR = "..\\run_files"
PEAR_FILE_NAME = "PEARINP.DRV"
MONO_FILE_NAME = "MONOINP.DRV"
file_name = "FSSAINP.DRV"
DATA_FILE_NAME = "FSSADATA.DAT"
p_FSS_DRV = os.path.join(RUN_FILES_DIR, file_name)
p_DATA_FILE = os.path.join(RUN_FILES_DIR, DATA_FILE_NAME)
INPUT_MATRIX_FORMAT = "(8F10.7)"

# Script paths
p_FSS_DIR = 'scripts/fssa-21'
test_p_FSS_DIR = '../lib/scripts/fssa-21'
SCRIPT_PEARSON = "PEARSON"
SCRIPT_MONO = "MONO"


def validate_input(i, var, lines):
    if i + var["line"] - 1 > len(lines):
        raise Exception(
            f"Invalid line number {var['line'] + 1}:"
            f"\n The line "
            "number is greater than the number of "
            "lines in the file")
    if var["col"] - 1 > len(lines[i + var["line"] - 1]):
        raise Exception(f"Invalid column number "
                        f"{var['col']} in line"
                        f" {i + var['line']}:\n"
                        "The column "
                        "number is greater than the number of "
                        "columns in the file")
    if var["col"] - 1 + var["width"] > len(
            lines[var["line"] - 1]):
        raise Exception(f"Invalid width "
                        f"line: "
                        f"{i + var['line']} column"
                        f":{var['col']}, "
                        f"width:{var['width']}:\n "
                        f"The width is greater "
                        "than the number of columns in the "
                        "file")

def load_data_file(path, delimiter=None, lines_per_var=1, manual_format: List[
    dict] = None, safe_mode=False):
    """
    Load data file from path and return a pandas dataframe
    :param lines_per_var:
    :param path:
    :param delimiter:
    :param manual_format: [{line (1..n), col(1..n) , width(1..n), label} for
    each variable]
    :return:
    """
    if manual_format:
        if "line" not in manual_format[0] or \
                "col" not in manual_format[0] or \
                "width" not in manual_format[0]:
            raise Exception("Invalid manual format:\n Each variable must have "
                            "line, col and width")
    if not delimiter and not manual_format:
        raise Exception("Either delimiter or manual format must be specified")
    data = []
    with open(path, "r") as f:
        lines = f.readlines()
        if len(lines) % lines_per_var != 0:
            raise Exception("Invalid number of lines:\n It seems the number "
                            "of lines is not a multiple of the number of "
                            "lines per row")
        for i in range(0, len(lines), lines_per_var):
            row = []
            if manual_format:
                for var in manual_format:
                    if safe_mode:
                        validate_input(i, var, lines)
                    row.append(lines[i + var["line"] - 1][
                               var["col"] - 1:var["col"] - 1 + var["width"]])
            elif delimiter == DELIMITER_1_D:
                rrow = "".join(lines[i:i + lines_per_var]).strip().replace(
                    "\n", "")
                row = list(map(int, str(rrow)))
            elif delimiter == DELIMITER_2_D:
                rrow = "".join(lines[i:i + lines_per_var]).strip().replace(
                    "\n", "")
                row = [int(rrow[i:i + 2]) for i in range(0, len(rrow), 2)]
            else:
                rrow = "".join(lines[i:i + lines_per_var]).strip().replace(
                    "\n", "")
                row = rrow.split(delimiter)
            data.append(row)
    df = pd.DataFrame(data, columns=[i + 1 for i in range(len(data[0]))])
    return df


def get_random_data() -> pd.DataFrame:
    """
    This function generates random data matrix for the purpose of testing the
    :return:
    """
    n = np.random.randint(20, 31)
    m = np.random.randint(30, 31)
    data = np.random.randint(1, 10, (n, m))
    df = pd.DataFrame(data, columns=[i + 1 for i in range(len(data[0]))])
    return df


def run_fortran(corr_type,
                create_simplified_matrix_file="NUL"):
    def get_path(path: str):
        if os.path.exists(path):
            return os.path.abspath(path)
        else:
            return SCRIPT_NESTING_PREFIX + path

    # get the path's
    corr_input_drv_file = get_corr_input_file_path(corr_type)
    data_file = p_DATA_FILE
    fssa_input_drv_file = p_FSS_DRV
    output_matrix_file = p_OUTPUT_MAT_FILE
    output_results_file = p_OUTPUT_FILE
    script_corr_type = SCRIPT_MONO if corr_type == MONO else SCRIPT_PEARSON
    # script_nesting_prefix = SCRIPT_NESTING_PREFIX
    # def script_path(path: str): return script_nesting_prefix + path
    # p_FSS_DIR = 'scripts/fssa-21'
    # p_output = script_path(OUTPUT_DIR)
    # corr_type = "MONO"
    # corr_input_drv_file = "MONOINP.DRV"
    # data_file = "C:\\Users\\Raz_Z\\Desktop\\shmuel-project\\fssa-21\\GRAND.PRN"
    # create_simplified_matrix_file = 'NUL'
    # output_matrix_file = os.path.join(p_output,"MONOASC.MAT")
    # fssa_input_drv_file = "FSSAINP.DRV"
    # output_results_file = os.path.join(p_output, "DJK21.FSS")
    # corr_input_drv_file = r"C:\Users\Raz_Z\Desktop\shmuel-project\shared\simaple_example\MONOINP.DRV"
    # data_file = r"C:\Users\Raz_Z\Desktop\shmuel-project\shared" \
    #             r"\simaple_example\diamond6.txt"
    # create_simplified_matrix_file = 'NUL'
    # fssa_input_drv_file = r"C:\Users\Raz_Z\Desktop\shmuel-project\shared\simaple_example\FSSAINP.DRV"
    # output_matrix_file = r'C:\Users\Raz_Z\Desktop\shmuel-project\shared' \
    #                       r'\simaple_example\MONOASC.MAT'
    # output_results_file = r'C:\Users\Raz_Z\Desktop\shmuel-project\shared' \
    #                       r'\simaple_example\DJK21.FSS'

    # Define the command and arguments
    arguments = [
        script_corr_type,
        # Tells Fortran to run monotonicity coefficients on the
        # data. Replace by PEARSON if you want SSA to use Pearson
        # correlation coefficients instead.
        get_path(corr_input_drv_file),  # A file in a specific format (see
        # monoinp.drv
        # instructions file) that tells the program how to read data file
        # for computing the monotonicity coefficients. Replace by
        # PEARINP.DRV if you want SSA to use Pearson correlation coefficients.
        get_path(data_file),
        # Path and filename of the input data file in ASCII (simple txt
        # file). You can change it to fit with your own directory, and you
        # can simplify
        # filename. For example, c:\tstfssa\tstdata.dat
        create_simplified_matrix_file,  # Indicates that you don’t want the
        # program to produce a file with a simplified version of the
        # coefficient matrix. IF you do want such a file replace NUL by a
        # filename of your choice.
        get_path(output_matrix_file),  # is the name of the
        # coefficient-matrix-file
        # produce by the program
        get_path(fssa_input_drv_file),  # A file in a specific format (see
        # fssainp.drv
        # instructions file) that tells the program how to read data file and
        # what you want done.
        get_path(output_matrix_file),  # is the name of the
        # coefficient-matrix-file
        # produced by the program to be used by FSSA. It must be re-written
        # here; I don't know why.
        get_path(output_results_file)  # Path and filename of the output
        # data file. You can change it to your own directory, and simplify
        # filename. For example  c:\tstfssa\tstdata.fss
    ]
    # command = r"C:\Users\Raz_Z\Desktop\shmuel-project\fssa-21\FASSA.BAT"
    command = "FASSA.BAT"

    # Combine the command and arguments into a single list
    full_command = [command] + arguments

    # Run the command
    try:
        os.chdir(os.path.abspath(p_FSS_DIR))
    except FileNotFoundError:
        try:
            os.chdir(os.path.abspath(test_p_FSS_DIR))
        except FileNotFoundError:
            raise FileNotFoundError("FSSA script directory not found")
    result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    # Print the output and error, if any
    if result.returncode != 0:
        raise Exception(f"FSSA script failed : {result.stderr}")
    print("Output:", result.stdout)
    print("Error:", result.stderr)

def create_running_files(
        variables_labels: List[dict],
        correlation_type: str,
        data_matrix: List[List],
        min_dim: int = 2, max_dim: int = 2,
        is_similarity_data: bool = True, eps=0,
        missing_cells: list = [(99, 99)],
        iweigh=2, nfacet=0, ntface=0,
        store_coordinates_on_file: bool = False, iboxstring=0,
        default_form_feed=0, nmising: int = 0, nlabel: int = 0,
        iprfreq: bool = False, iintera: bool = False,
        facet_details = None,
        facet_var_details = None,
        hypotheses_details = None,
        facet_dim_details = None,
        valid_values_range = None
):
    """
    This function creates the running files for FSSA program
    :return:
    """
    # Create the FSSA input file
    create_fssa_input_file(
        variables_labels,
        min_dim,
        max_dim,
        is_similarity_data,
        eps,
        missing_cells,
        iweigh,
        nfacet,
        ntface,
        store_coordinates_on_file,
        iboxstring,
        default_form_feed,
        facet_details,
        facet_var_details,
        hypotheses_details,
        facet_dim_details)

    # Create the FSSA matrix file
    create_corr_input_file(
        correlation_type,
        variables_labels,
        nlabel,
        iprfreq,
        iintera,
        valid_values_range,
    )
    # Create the FSSA data file
    create_fssa_data_file(data_matrix)


def create_fssa_data_file(data_matrix: List[List[int]]):
    """
    This function creates the FSSA data file (FSSADATA.DAT) for the FSSA
    program
    :param data_matrix: the data matrix
    :return:
    """

    # Create the data file
    def parse_item_2d(item):
        try:
            if len(str(item)) < 2:
                return str(item) + " "
            return str(item)
        except ValueError:
            return " "

    with open(p_DATA_FILE, 'w', encoding="ascii") as f:
        for row in data_matrix:
            f.write("".join(map(parse_item_2d, row)) + "\n")


def create_fssa_input_file(
        # variables_details,
        variables_labels: List[Dict],
        min_dim: int = 2,
        max_dim: int = 2,
        is_similarity_data: bool = True,
        eps=0,
        missing_cells: list = [(99, 99)],
        iweigh=2,
        nfacet=0,
        ntface=0,
        store_coordinates_on_file: bool = False,
        iboxstring=0,
        default_form_feed=0,
        facet_details=None,
        facet_var_details=None,
        hypotheses_details=None,
        facet_dim_details=None,):
    """
This function creates the FSSA input file (FSSAINP.DRV) for the FSSA program
    :param variables_labels:
    :param min_dim: the minimum dimension of the data matrix
    :param max_dim: the maximum dimension of the data matrix
    :param is_similarity_data: a boolean variable indicating whether the data
    is similarity data or not
    :param eps:
    :param missing_cells: a list of tuples, each tuple contains a range of
    values to be considered as missing cells
    :param iweigh: an integer variable indicating the weighing method
    :param nfacet: an integer variable indicating the number of facets
    :param ntface: an integer variable indicating the number of t-faces
    :param store_coordinates_on_file: a boolean variable indicating whether
    the plotted coordinates should be stored on a file or not
    :param iboxstring: an integer variable indicating the boxstring
    :param default_form_feed: an integer variable indicating the default form
    feed
    :return: None
    """
    # checks if the directory RUN_FILES_DIR exists, if not creates it in the
    # root directory
    if not os.path.exists(RUN_FILES_DIR):
        os.makedirs(RUN_FILES_DIR)
    nvar = len(variables_labels)
    with open(p_FSS_DRV, "w") as f:
        f.write("FSSA-24 INPUT FILE\n")
        f.write(f"  {nvar}   {min_dim}   {max_dim}")
        f.write(f"   {int(is_similarity_data)}   {eps}   "
                f"{len(missing_cells)}")
        f.write(f"   {iweigh}  {nvar}   {nfacet}  "
                f" {ntface}   1")
        f.write(f"   {int(store_coordinates_on_file)}   {iboxstring}")
        f.write(f"   {default_form_feed}\n   {len(missing_cells)}")
        for missing_cell_range in missing_cells:
            f.write(
                f" {missing_cell_range[0]:.7f} {missing_cell_range[1]:.7f}")
        f.write("\n")
        f.write(INPUT_MATRIX_FORMAT + "\n")
        for variable in variables_labels:
            f.write(f" {' ' if variable['index'] < 10 else ''}"
                    f" {variable['index']} "
                    f" {variable['label']}\n")
        # facet variable details
        for variable in facet_var_details:
            for var_facet in variable:
                f.write(f" {var_facet}")
            f.write("\n")
        # facet details
        for facet_labels in facet_details:
            f.write(f"   {len(facet_labels)}")
        f.write("\n")
        for facet_labels in facet_details:
            [f.write(f"{label}\n") for label in facet_labels]
        # hypotheses details
        write_hypotheses(f, facet_dim_details, hypotheses_details)

def write_hypotheses(f, facet_dim_details, hypotheses_details):
    """
    This function writes the hypotheses details to the FSSA input file
    :param facet_dim_details:
    :param hypotheses_details:
    :return:
    """
    for dim, facets in facet_dim_details.items():
        dim_axes = list(range(1, dim + 1))
        axes_pairs = [(a, b) for idx, a in enumerate(dim_axes) for b in
                      dim_axes[idx + 1:]]
        for facet_i, facet in enumerate(facets):
            for a, b in axes_pairs:
                if dim == 2:
                    for model in hypotheses_details[facet_i]:
                        f.write(f"   {dim}   {facet}   {a}   {b}   {model}\n")
                else:
                    f.write(f"   {dim}   {facet}   {a}   {b}   0\n")


def get_corr_input_file_path(correlation_type: str):
    file_name = MONO_FILE_NAME if correlation_type == MONO else PEAR_FILE_NAME
    # checks if the directory RUN_FILES_DIR exists, if not creates it in the
    # root directory
    if not os.path.exists(RUN_FILES_DIR):
        os.makedirs(RUN_FILES_DIR)
    return os.path.join(RUN_FILES_DIR, file_name)


def create_corr_input_file(correlation_type: str,
                           variables_details: List[Dict],
                           nlabel: int = 0,
                           iprfreq: bool = False,
                           iintera: bool = False,
                           valid_values_range = [] ):
    """
    :param correlation_type:
    :param nmising:
    :param nlabel:
    :param iprfreq:
    :param iintera:
    :param variables_details: start column, width
    :param valid_values_range:
    :param variables_labels:
    :return:
    """
    # checks if the directory RUN_FILES_DIR exists, if not creates it in the
    if not os.path.exists(RUN_FILES_DIR):
        os.makedirs(RUN_FILES_DIR)
    file_path = get_corr_input_file_path(correlation_type)
    with open(file_path, "w") as f:
        f.write("FSSA\n")
        f.write(f"   {len(variables_details)}   {len(valid_values_range)}   {nlabel}   "
                f"{int(iprfreq)}   {int(iintera)}\n")
        # variables details
        var_txt = "("
        for i, var in enumerate(variables_details):
            if i > 0: var_txt += ","
            var_txt += f"T{ENTRY_WIDTH * i + 1}I{ENTRY_WIDTH}"
        # add "\n"
        for i in range(80, len(var_txt), 81):
            var_txt = var_txt[:i] + "\n" + var_txt[i:]
        f.write(var_txt)
        f.write(")\n")
        #
        if valid_values_range:
            missing_values = parse_missing_values(valid_values_range)
            for i, missing_value in enumerate(missing_values):
                f.write(f"  {' ' if i+1 < 10 else ''}{i+1}"
                        f"   {len(missing_value)}")
                for value in missing_value:
                    f.write(f"   {value[0]}   {value[1]}")
                f.write("\n")
        # Looks like it is not implemented in the fortran code
        if nlabel:
            f.write(f"VARIABLE LABELS PLACEHOLDER\n")


if __name__ == '__main__':
    # load_data_file("C:\\Users\\Raz_Z\\Desktop\\shmuel-project\\fssa-21\\GRAND.PRN")
    # load_data_file("scripts/simaple_example/diamond6.txt")
    # run_fortran()
    # a = get_random_data()
    # a = load_data_file(r"C:\Users\Raz_Z\Desktop\shmuel-project\shared"
    #                    r"\simaple_example\diamond6.txt")
    # print(a)
    # variables_details = [
    #     {"index": 1, "label": "A", "start_col": 1, "width": 1},
    #     {"index": 2, "label": "B", "start_col": 2, "width": 1},
    #     {"index": 3, "label": "C", "start_col": 3, "width": 1},
    #     {"index": 4, "label": "D", "start_col": 4, "width": 1},
    #     {"index": 5, "label": "E", "start_col": 5, "width": 1},
    #     {"index": 6, "label": "F", "start_col": 6, "width": 1}
    # ]
    # create_fssa_input_file(variables_details)
    # create_corr_input_file("MONO", variables_details)
    # np.random.seed(0)
    # data = get_random_data().values
    # create_fssa_data_file(data)
    # corr_type = "Monotonicity"
    # run_fortran(corr_type=corr_type)
    # path = r"C:\\Users\\Raz_Z\\Desktop\\shmuel-project\\fssa-21\\GRAND.PRN"
    # path = r"C:\Users\Raz_Z\Desktop\shmuel-project\shared\example_3\babystu4.prn"
    path = r"C:\Users\Raz_Z\Desktop\shmuel-project\shared\simaple_example\diamond6.txt"
    load_data_file(path, delimiter=",", lines_per_var=2)
