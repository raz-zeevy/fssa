import os

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 750

DELIMITER_1_D = "1d"
DELIMITER_2_D = "2d"

MONO = "Monotonicity"
PEARSON = "Pearson"
ENTRY_WIDTH = 2

######################
#        FSS         #
######################
# Script paths
p_FSS_DIR = './scripts/fssa-21'
SCRIPT_PEARSON = "PEARSON"
SCRIPT_MONO = "MONO"


def get_script_dir_path():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        fss_dir = os.path.join(base_dir, p_FSS_DIR)
    except FileNotFoundError:
        raise FileNotFoundError("FSSA script directory not found")
    return fss_dir


# Output Paths
SCRIPT_NESTING_PREFIX = "..\\..\\..\\"
p_OUTPUT_DIR = "output"
OUTPUT_MONO_MAT_FILE = "MONOASC.MAT"
OUTPUT_PEARSON_MAT_FILE = "PEARASC.MAT"
OUTPUT_FILE_NAME = "DJK21.FSS"
p_OUTPUT_FILE = os.path.join(p_OUTPUT_DIR, OUTPUT_FILE_NAME)

# Input paths
RUN_FILES_DIR = "..\\run_files"
RUN_FILES_DIR = os.path.join(get_script_dir_path(), RUN_FILES_DIR)
PEAR_FILE_NAME = "PEARINP.DRV"
MONO_FILE_NAME = "MONOINP.DRV"
file_name = "FSSAINP.DRV"
DATA_FILE_NAME = "FSSADATA.DAT"
p_FSS_DRV = os.path.join(RUN_FILES_DIR, file_name)
p_DATA_FILE = os.path.join(RUN_FILES_DIR, DATA_FILE_NAME)
INPUT_MATRIX_FORMAT = "(8F10.7)"

# Results

RESULTS_SUCCESS_STDERR = """STOP NEWMON terminated successfully
Note: The following floating-point exceptions are signalling: IEEE_DENORMAL
STOP SSA terminated successfully.
"""
