from typing import List, Dict, Tuple
from lib.utils import *

class CorrelationInputWriter:
    def __init__(self):
        pass

    def create_corr_input_file(self, correlation_type: str,
                               variables_details: List[Dict],
                               nlabel: int = 0,
                               iprfreq: bool = False,
                               iintera: bool = False,
                               valid_values_range=[]):
        # checks if the directory RUN_FILES_DIR exists, if not creates it in the
        if not os.path.exists(RUN_FILES_DIR):
            os.makedirs(RUN_FILES_DIR)
        file_path = self.get_corr_input_file_path(correlation_type)
        var_width = 'F' if correlation_type == PEARSON else 'I'
        with open(file_path, "w") as f:
            f.write("FSSA\n")
            f.write(
                f"  {len(variables_details)}  {len(valid_values_range)}   {nlabel}   "
                f"{int(iprfreq)}   {int(iintera)}\n")
            # variables details
            var_txt = "("
            for i, var in enumerate(variables_details):
                if i > 0: var_txt += ","
                var_txt += f"T{ENTRY_WIDTH * i + 1}{var_width}{ENTRY_WIDTH}"
            # add "\n"
            for i in range(80, len(var_txt), 81):
                var_txt = var_txt[:i] + "\n" + var_txt[i:]
            f.write(var_txt)
            f.write(")\n")
            #
            if valid_values_range:
                missing_values = self.parse_missing_values(valid_values_range)
                for i, missing_value in enumerate(missing_values):
                    f.write(f"  {' ' if i + 1 < 10 else ''}{i + 1}"
                            f"   {len(missing_value)}")
                    for value in missing_value:
                        f.write(f"   {value[0]}   {value[1]}")
                    f.write("\n")
            # Looks like it is not implemented in the fortran code
            if nlabel:
                f.write(f"VARIABLE LABELS PLACEHOLDER\n")

    @staticmethod
    def get_corr_input_file_path(correlation_type: str):
        file_name = MONO_FILE_NAME if correlation_type == MONO else PEAR_FILE_NAME
        # checks if the directory RUN_FILES_DIR exists, if not creates it in the
        # root directory
        if not os.path.exists(RUN_FILES_DIR):
            os.makedirs(RUN_FILES_DIR)
        return os.path.join(RUN_FILES_DIR, file_name)

    def parse_missing_values(self, valid_values_range: List[Tuple]):
        var_missing_values = []
        for var in valid_values_range:
            intervals = []
            low, high = int(var[0]), int(var[1])
            max_num = 99 if high > 9 else 9
            min_num = 0
            if low > min_num:
                intervals.append((min_num, low-1))
            if high < max_num:
                intervals.append((high+1, max_num))
            var_missing_values.append(intervals)
        return var_missing_values

