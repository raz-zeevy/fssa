# Python code to run the specified command using subprocess

import subprocess
import os
from typing import List, Tuple, Dict

import numpy as np
import pandas as pd
from lib.utils import *

INPUT_MATRIX_FORMAT = "(8F10.7)"
OUTPUT_DIR = "output"
RUN_FILES_DIR = "..\\run_files"


def load_data_file(path, delimiter):
    if delimiter == DELIMITER_1_D:
        data = np.loadtxt(path, dtype="int")
        split_data = [list(map(int, str(row))) for row in data]
        data = split_data
    else:
        data = np.loadtxt(path, delimiter=delimiter, dtype="int",
                          )
    df = pd.DataFrame(data)
    return df


def get_random_data() -> pd.DataFrame:
    """
    This function generates random data matrix for the purpose of testing the
    :return:
    """
    n = np.random.randint(4, 5)
    m = np.random.randint(4, 5)
    data = np.random.randint(1, 10, (n, m))
    df = pd.DataFrame(data)
    return df


def run_fortran():
    script_nesting_prefix = "..\\..\\..\\"

    def script_path(path: str): return script_nesting_prefix + path

    p_FSS_DIR = 'scripts/fssa-21'

    p_output = script_path(OUTPUT_DIR)

    # corr_type = "MONO"
    # corr_input_drv_file = "MONOINP.DRV"
    # data_file = "C:\\Users\\Raz_Z\\Desktop\\shmuel-project\\fssa-21\\GRAND.PRN"
    # create_simplified_matrix_file = 'NUL'
    # output_matrix_file = os.path.join(p_output,"MONOASC.MAT")
    # fssa_input_drv_file = "FSSAINP.DRV"
    # output_results_file = os.path.join(p_output, "DJK21.FSS")

    # corr_type = "PEARSON"
    corr_type = "MONO"
    corr_input_drv_file = r"C:\Users\Raz_Z\Projects\Shmuel\FSS\MONOINP.DRV"
    data_file = r"C:\Users\Raz_Z\Desktop\shmuel-project\shared" \
                r"\simaple_example\diamond6.txt"
    create_simplified_matrix_file = 'NUL'
    output_matrix_file = os.path.join(p_output, "MONOASC.MAT")
    fssa_input_drv_file = r"C:\Users\Raz_Z\Projects\Shmuel\FSS\FSSAINP.DRV"
    output_results_file = os.path.join(p_output, "DJK21.FSS")

    # Define the command and arguments
    command = "FASSA.BAT"
    arguments = [
        corr_type,  # Tells Fortran to run monotonicity coefficients on the
        # data. Replace by PEARSON if you want SSA to use Pearson
        # correlation coefficients instead.
        corr_input_drv_file,  # A file in a specific format (see monoinp.drv
        # instructions file) that tells the program how to read data file
        # for computing the monotonicity coefficients. Replace by
        # PEARINP.DRV if you want SSA to use Pearson correlation coefficients.
        data_file,
        # Path and filename of the input data file in ASCII (simple txt
        # file). You can change it to fit with your own directory, and you
        # can simplify
        # filename. For example, c:\tstfssa\tstdata.dat
        create_simplified_matrix_file,  # Indicates that you don’t want the
        # program to produce a file with a simplified version of the
        # coefficient matrix. IF you do want such a file replace NUL by a
        # filename of your choice.
        output_matrix_file,  # is the name of the coefficient-matrix-file
        # produce by the program
        fssa_input_drv_file,  # A file in a specific format (see fssainp.drv
        # instructions file) that tells the program how to read data file and
        # what you want done.
        output_matrix_file,  # is the name of the coefficient-matrix-file
        # produced by the program to be used by FSSA. It must be re-written
        # here; I don't know why.
        output_results_file  # Path and filename of the output
        # data file. You can change it to your own directory, and simplify
        # filename. For example  c:\tstfssa\tstdata.fss
    ]

    # Combine the command and arguments into a single list
    full_command = [command] + arguments

    # Run the command
    os.chdir(p_FSS_DIR)
    result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)

    # Print the output and error, if any
    print("Output:", result.stdout)
    print("Error:", result.stderr)


def create_running_files(
        variables_details: List[Dict],
        correlation_type: str,
        data_matrix: List[List],
        min_dim: int = 2, max_dim: int = 2,
        is_similarity_data: bool = True, eps=0,
        missing_cells: list = [(99, 99)],
        iweigh=2, nfacet=0, ntface=0,
        store_coordinates_on_file: bool = False, iboxstring=0,
        default_form_feed=0, nmising: int = 0, nlabel: int = 0,
        iprfreq: bool = False, iintera: bool = False,
        missing_values: str = 0,
):
    """
    This function creates the running files for FSSA program
    :return:
    """
    # Create the FSSA input file
    create_fssa_input_file(
        variables_details,
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
        default_form_feed)

    # Create the FSSA matrix file
    create_corr_input_file(
        correlation_type,
        variables_details,
        nmising,
        nlabel,
        iprfreq,
        iintera,
        missing_values,
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
        if item < 10:
            return "0" + str(item)
        return str(item)

    file_path = os.path.join(RUN_FILES_DIR, "FSSADATA.DAT")
    with open(file_path, 'w', encoding="ascii") as f:
        for row in data_matrix:
            f.write("".join(map(parse_item_2d, row)) + "\n")

def create_fssa_input_file(
        variables_details,
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
        default_form_feed=0):
    """
This function creates the FSSA input file (FSSAINP.DRV) for the FSSA program
    :param variables_details: a list of tuples, each tuple contains the
    variable name and the variable type (either "N" or "O")
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
    file_name = "FSSAINP.DRV"
    if not os.path.exists(RUN_FILES_DIR):
        os.makedirs(RUN_FILES_DIR)
    file_path = os.path.join(RUN_FILES_DIR, file_name)
    with open(file_path, "w") as f:
        f.write("FSSA-24 INPUT FILE\n")
        f.write(f"   {len(variables_details)}   {min_dim}   {max_dim}")
        f.write(f"   {int(is_similarity_data)}   {eps}   "
                f"{len(missing_cells)}")
        f.write(f"   {iweigh}   {len(variables_details)}   {nfacet}  "
                f" {ntface}   1")
        f.write(f"   {int(store_coordinates_on_file)}   {iboxstring}")
        f.write(f"   {default_form_feed}\n   {len(missing_cells)}")
        for missing_cell_range in missing_cells:
            f.write(
                f" {missing_cell_range[0]:.7f} {missing_cell_range[1]:.7f}")
        f.write("\n")
        f.write(INPUT_MATRIX_FORMAT + "\n")
        for variable in variables_details:
            f.write(f"   {variable['index']}  {variable['label']}\n")


def create_corr_input_file(correlation_type: str,
                           variables_details: List[Dict],
                           nmising: int = 0,
                           nlabel: int = 0,
                           iprfreq: bool = False,
                           iintera: bool = False,
                           missing_values: str = 0, ):
    """
    :param correlation_type:
    :param nmising:
    :param nlabel:
    :param iprfreq:
    :param iintera:
    :param variables_details: start column, width
    :param missing_values:
    :param variables_labels:
    :return:
    """
    file_name = "MONOINP.DRV" if correlation_type == "MONO" else "PEARINP.DRV"
    # checks if the directory RUN_FILES_DIR exists, if not creates it in the
    # root directory
    if not os.path.exists(RUN_FILES_DIR):
        os.makedirs(RUN_FILES_DIR)
    file_path = os.path.join(RUN_FILES_DIR, file_name)
    with open(file_path, "w") as f:
        f.write("FSSA\n")
        f.write(f"   {len(variables_details)}   {nmising}   {nlabel}   "
                f"{int(iprfreq)}   {int(iintera)}\n")
        f.write("(")
        for i, var in enumerate(variables_details):
            if i > 0: f.write(",")
            f.write(f"T{2*i+1}I{2}")
        f.write(")\n")
        if nmising:
            f.write(f"{missing_values}\n")
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
    np.random.seed(0)
    data = get_random_data().values
    create_fssa_data_file(data)
