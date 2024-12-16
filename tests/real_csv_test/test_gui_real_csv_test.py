"""
The purpose of this test is to test the GUI with a real csv file that
contains:
- Missing values
- Different types of variables, some of them are numerical and some aren't
- numerical variables that need recoding
"""

from lib.controller.controller import *
from lib.controller.controller import Controller
from lib.fss.fss_input_parser import *
from lib.utils import *

DATA_PATH = 'data.csv'
SET_MODE_TEST()
# SET_MODE_PRODUCTION()

class simple_example_gui(Controller):
    def __init__(self):
        super().__init__()
        self.test_simple_example()

    def test_simple_example(self):
        self.gui.pages[START_PAGE_NAME].button_recorded_data.invoke()
        # get the absoult path of the data file
        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(test_dir_path,
                                      DATA_PATH)
        self.gui.pages[INPUT_PAGE_NAME].set_data_file_path(
            data_file_path)
        self.set_header(True)
        self.data_file_extension = ".csv"
        self.load_csv_init()
        self.gui.pages[INPUT_PAGE_NAME].disable_additional_options()
        self.next_page()
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].select_variables_window(
            {i for i in range(3, 21)}
        )
        self.next_page()
        #
        self.gui.show_recode_window()
        self.gui.recode_window.set_variables_indices("9")
        recoding_pairs = [
            (10,1),
            (20,2),
            (30,3),
            (40,4),
            (60,6),
            ("100-10000",10),
        ]
        for pair in recoding_pairs:
            self.gui.recode_window.add_pair(*pair)
        self.gui.recode_window.apply_recoding()
        #
        self.gui.show_recode_window()
        self.gui.recode_window.set_variables_indices("1-8")
        self.gui.recode_window.set_inverse(True)
        self.gui.recode_window.apply_recoding()
        self.gui.show_recode_history_window()
        # close the recoding history window
        self.gui.recode_history_window.destroy()
        self.next_page()
        self.next_page()
        try:
            self.output_path = \
                r"C:\Users\Raz_Z\Projects\Shmuel\fssaDist\fssa\output" \
                r"\real_csv.fss"
            self.run_fss(self._run_fss)
            self.enable_view_results()
        except Exception as e:
            print(e)
            raise(e)
        # # run_file_path = p_FSS_DRV
        # # true_file_path = os.path.join(test_dir_path, "FSSAINP.DRV")
        # # assert diff_lines_num(run_file_path, true_file_path) == 1
        assert os.path.isfile(self.output_path)

if __name__ == '__main__':
    a = simple_example_gui()
    a.run_process()