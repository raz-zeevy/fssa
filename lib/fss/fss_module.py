# Python code to run the specified command using subprocess

import subprocess
import pandas as pd

from lib.fss.fss_corr_input_writer import CorrelationInputWriter
from lib.fss.fss_input_writer import FssInputWriter
from lib.fss.fss_input_parser import *
from lib.utils import *


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
                output_path,
                create_simplified_matrix_file="NUL"):
    def get_path(path: str):
        if os.path.exists(path):
            return os.path.abspath(path)
        else:
            return SCRIPT_NESTING_PREFIX + path
    # get the path's
    corr_input_drv_file = CorrelationInputWriter.get_corr_input_file_path(
        corr_type)
    data_file = p_DATA_FILE
    fssa_input_drv_file = p_FSS_DRV
    matrix_file_name = OUTPUT_MONO_MAT_FILE if corr_type == MONO else \
        OUTPUT_PEARSON_MAT_FILE
    output_results_file = output_path
    output_matrix_file = os.path.join(os.path.dirname(output_results_file)
                                        , matrix_file_name)
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
        output_matrix_file,  # is the name of the
        # coefficient-matrix-file
        # produce by the program
        get_path(fssa_input_drv_file),  # A file in a specific format (see
        # fssainp.drv
        # instructions file) that tells the program how to read data file and
        # what you want done.
        output_matrix_file,  # is the name of the
        # coefficient-matrix-file
        # produced by the program to be used by FSSA. It must be re-written
        # here; I don't know why.
        output_results_file  # Path and filename of the output
        # data file. You can change it to your own directory, and simplify
        # filename. For example  c:\tstfssa\tstdata.fss
    ]
    # command = r"C:\Users\Raz_Z\Desktop\shmuel-project\fssa-21\FASSA.BAT"
    command = "FASSA.BAT"

    # Combine the command and arguments into a single list
    full_command = [command] + arguments

    # Run the command
    fss_dir = get_script_dir_path()
    os.chdir(fss_dir)
    result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    # Print the output and error, if any
    if result.returncode != 0:
        raise Exception(f"FSSA script failed : {result.stderr}")
    if result.stderr != RESULTS_SUCCESS_STDERR:
        raise Exception(f"FSSA script failed : {result.stderr}")
    print("Output:", result.stdout)
    print("Error:", result.stderr)

def create_running_files(
        job_name : str,
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
    fssi = FssInputWriter()
    fssi.create_fssa_input_file(
        job_name,
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
    corri = CorrelationInputWriter()
    corri.create_corr_input_file(
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
