# Python code to run the specified command using subprocess

import subprocess
from typing import List
import numpy as np
import pandas as pd
from contextlib import contextmanager
from lib.fss.fss_corr_input_writer import CorrelationInputWriter
from lib.fss.fss_input_writer import FssInputWriter
from lib.utils import *

OUT_HEADER = """ECHO OFF \nECHO is off.\n            *******************************************************\n            *                                                     *\n            *              F A C E T E D    S S A                 *\n            *                                                     *\n            *******************************************************\n"""

OUT_HEADER_PEASEON = "ECHO OFF \nECHO is off.\n            *******************************************************\n            *                                                     *\n            *              F A C E T E D    S S A                 *\n            *                                                     *\n            *******************************************************\nECHO is off.\nECHO is off.\n"""

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


def load_recorded_data(path, delimiter=None, lines_per_var=1, manual_format: List[
    dict] = None, safe_mode=False, extension=None,
                       has_header=False):
    """
    Load data file from path and return a pandas dataframe
    :param lines_per_var:
    :param path:
    :param delimiter:
    :param manual_format: [{line (1..n), col(1..n) , width(1..n), label} for
    each variable]
    :return:
    """
    def load_supported_formats(extension):
        header = 0 if has_header else None

        # Load the file based on the extension
        if extension == ".csv":
            df = pd.read_csv(path, sep=",", header=header, dtype=str)
        elif extension == ".tsv":
            df = pd.read_csv(path, sep="\t", header=header, dtype=str)
        elif extension == ".xls" or extension == ".xlsx":
            df = pd.read_excel(path,
                               header=header,
                               engine="openpyxl",
                               dtype=str)
        else:
            raise Exception(f"Invalid extension: {extension}")

        # Set default column names if there is no header
        if header is None:
            df.columns = [f"var{i + 1}" for i in df.columns]

        # Remove rows that are completely empty
        df.dropna(how="all", inplace=True)

        # Replace NaN values with an empty string
        df.fillna("", inplace=True)
        return df

    def load_other_formats():
        data = []
        failed_rows = []
        with open(path, "r") as f:
            lines = f.readlines()
            if len(lines) % lines_per_var != 0:
                raise Exception(
                    "Invalid number of lines:\n It seems the number "
                    "of lines is not a multiple of the number of "
                    "lines per row")
            for i in range(0, len(lines), lines_per_var):
                if not lines[i].strip():
                    continue
                try:
                    row = []
                    if manual_format:
                        for var in manual_format:
                            if safe_mode:
                                validate_input(i, var, lines)
                            row.append(lines[i + var["line"] - 1][
                                       var["col"] - 1:var["col"] - 1 + var[
                                           "width"]])
                    elif delimiter == DELIMITER_1_D:
                        rrow = "".join(
                            lines[i:i + lines_per_var]).strip().replace(
                            "\n", "")
                        row = list(rrow)
                    elif delimiter == DELIMITER_2_D:
                        rrow = "".join(
                            lines[i:i + lines_per_var]).strip().replace(
                            "\n", "")
                        row = [rrow[i:i + 2] for i in
                               range(0, len(rrow), 2)]
                    else:
                        rrow = "".join(
                            lines[i:i + lines_per_var]).strip().replace(
                            "\n", "")
                        row = rrow.split(delimiter)
                except:
                    failed_rows.append(i + 1)
                if row:
                    data.append(row)
        for line in data:
            if line: break
        else:
            raise DataLoadingException("bad file")
        if failed_rows:
            import warnings
            if len(failed_rows) > 10:
                warnings.warn("Failed to load the following rows: "
                              f"["
                              f"{','.join([str(i) for i in failed_rows[:9]])}..."
                              f"{failed_rows[-1]}]")
            else:
                warnings.warn("Failed to load the following rows: "
                              f"{failed_rows}")
        longest_row = max([len(row) for row in data])
        df = pd.DataFrame(data, columns=[f"var{i + 1}" for i in
                                         range(longest_row)])
        df.fillna("", inplace=True)
        return df

    if manual_format:
        if "line" not in manual_format[0] or \
                "col" not in manual_format[0] or \
                "width" not in manual_format[0]:
            raise Exception("Invalid manual format:\n Each variable must have "
                            "line, col and width")
    if not delimiter and not manual_format and not extension:
        raise Exception("Recorded data loader don't have enough information "
                        "to load the file")
    if extension:
        return load_supported_formats(extension)
    return load_other_formats()


def load_matrix_data(path, matrix_details) -> pd.DataFrame:
    entries_num_in_row = matrix_details["entries_num_in_row"]
    var_num = matrix_details["var_num"]
    # Step 1: Read the file content
    with open(path, 'r') as file:
        file_content = file.read()

    # Step 2: Convert the string of numbers into a list of integers or floats
    numbers = [float(num) for num in file_content.split()]

    # Calculate the total number of logical rows based on the total entries and number of columns
    num_logical_rows = len(numbers) // var_num

    # Step 3: Convert the list into a numpy array
    matrix = np.array(numbers)

    # Step 4: Reshape the array into the desired shape based on the number of logical rows and columns
    matrix = matrix.reshape((num_logical_rows, var_num))

    # Convert to pandas DataFrame (optional)
    df = pd.DataFrame(matrix, columns=[i + 1 for i in range(len(matrix[0]))])

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

def parse_fortran_output(result: subprocess.CompletedProcess):
        # Print the output and error, if any
    if result.returncode != 0:
        raise Exception(f"FSSA script failed : {result.stderr}")
    if "SSA terminated successfully" in result.stderr:
        return
    edited_output = result.stdout.replace(OUT_HEADER, "").replace(OUT_HEADER_PEASEON, "").replace("ECHO is off.", "")
    if result.stderr not in [RESULTS_SUCCESS_STDERR,
                                RESULTS_SUCCESS_STDERR2,
                                RESULTS_SUCCESS_STDERR3]:
        if "Fortran runtime error:" in result.stderr:
            raise Exception(f"FSSA script failed : {result.stderr}")
        if len(result.stderr.split("\n")) >= 3:
            if result.stderr.split("\n")[2] == 'Fortran runtime error: ' \
                                                'Cannot write to file opened for READ':
                exception = result.stderr.split('\n')[2]
                raise Exception(exception)
            elif "Segmentation fault - invalid memory reference" in result.stderr:
                raise Exception(f"FSSA script failed : Memory error. Please check the input file, variables and the missing values (if not specified, set to '0')")
            else:
                raise Exception(f"FSSA script failed : {result.stderr} {edited_output}")
        else:
            raise Exception(f"FSSA script failed : {result.stderr} {edited_output}")
    print("Output:", result.stdout)
    print("Error:", result.stderr)


def create_fssacmd_bat(fss_dir: str, arguments: List[str]):
    """
    arguments: the arguments to run the fssa program can be of different lengths
    """
    fssacmd_path = os.path.join(os.path.dirname(p_DATA_FILE), "fssacmd.bat")
    with open(fssacmd_path, "w") as f:
        f.write(f"cd {fss_dir}\n")
        f.write(f"FASSA.BAT {' '.join(arguments)}")

def run_matrix_fortran(output_path: str):
    def get_path(path: str):
        if os.path.exists(path):
            return os.path.abspath(path)
        else:
            return SCRIPT_NESTING_PREFIX + path
    data_file = p_DATA_FILE
    fssa_input_drv_file = p_FSS_DRV
    output_results_file = output_path

    # Define the command and arguments
    arguments = [
        get_path(fssa_input_drv_file),  # A file in a specific format (see
        # fssainp.drv
        # instructions file) that tells the program how to read data file and
        # what you want done.
        get_path(data_file),
        # Path and filename of the input data file in ASCII (simple txt
        # file). You can change it to fit with your own directory, and you
        # can simplify
        # filename. For example, c:\tstfssa\tstdata.dat
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
    create_fssacmd_bat(fss_dir, arguments)
    with cwd(fss_dir):
        result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)
        # Print the output and error, if any
        parse_fortran_output(result)

        
def run_fortran(corr_type,
                output_path,
                create_simplified_matrix_file="NUL", debug=False):
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
    #
    output_matrix_file = os.path.join(os.path.dirname(p_DATA_FILE)
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
    create_fssacmd_bat(fss_dir, arguments)
    if debug:
        print(f"full_command: {full_command}")
        open_fss_files_dir()
        input("Press Enter to continue...")
    with cwd(fss_dir):
        result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)
        # Print the output and error, if any
        parse_fortran_output(result)


@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)

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
                return str(item) + " "*(2-len(str(item)))
            return str(item)
        except ValueError:
            return " "

    with open(p_DATA_FILE, 'w', encoding="ascii") as f:
        for row in data_matrix:
            f.write("".join(map(parse_item_2d, row)) + "\n")


def create_fss_matrix_file(matrix_details: dict, matrix_path: str):
   matrix = np.loadtxt(matrix_path).reshape(matrix_details['var_num'],-1).tolist()
   # matrix = np.around(matrix, matrix_details['decimal_places'])
   precision = f".{matrix_details['decimal_places']}f"
   spacing = matrix_details['field_width']
   def parse_item(item):
       if item >= 0:
           res = f"{item:{precision}}" if (item > 9) else f"" \
                                                              f"0{item:{precision}}"
       else:
              res = f"{item:{precision}}" if (item < -9) else f"" \
                                                                f"-0{abs(item):{precision}}"
       return (spacing - 1 - len(res)) * " " + str(res)

   for i in range(len(matrix)):
       matrix[i] = " ".join(map(parse_item, matrix[i]))
   with open(p_DATA_FILE, 'w', encoding="ascii") as f:
       f.writelines(row + "\n" for row in matrix)

def create_matrix_running_files(
        job_name : str,
        variables_labels: List[dict],
        correlation_type: str,
        matrix_details: dict,
        matrix_path: str,
        min_dim: int = 2,
        max_dim: int = 2,
        eps=0,
        missing_cells: list = [(99, 99)],
        iweigh=2, nfacet=0, ntface=0,
        store_coordinates_on_file: bool = False, iboxstring=0,
        default_form_feed=0, nmising: int = 0, nlabel: int = 0,
        iprfreq: bool = False, iintera: bool = False,
        facet_details = None,
        facet_var_details = [],
        hypotheses_details = None,
        facet_dim_details = None,
):
    """
    This function creates the running files for FSSA program
    :return:
    """

    is_similarity_data = correlation_type == SIMILARITY
    input_matrix_format = f"({matrix_details['entries_num_in_row']}F" \
                          f"{matrix_details['field_width']}." \
                          f"{matrix_details['decimal_places']})"
    missing_cells = matrix_details['missing_ranges']
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
        facet_dim_details,
        input_matrix_format)

    # Create the FSSA Partial Matrix File
    create_fss_matrix_file(matrix_details, matrix_path)

def open_fss_files_dir():
    os.startfile(os.path.dirname(p_DATA_FILE))

if __name__ == '__main__':
    # Example usage
    # Example usage
    from lib.fss.convert_to_doc import output_to_word
    output_path = r"C:\Users\Raz_Z\Desktop\shmuel-project\shared\example_3" \
                  r"\BABY3D84.FSS"  # Path to your text file
    output_to_word(output_path)
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
    # path = r"C:\Users\Raz_Z\Desktop\shmuel-project\shared\simaple_example\diamond6.txt"
    # load_data_file(path, delimiter=",", lines_per_var=2)
