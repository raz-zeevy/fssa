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
from const import *


DATA_PATH = 'data.csv'
# SET_MODE_TEST()
SET_MODE_PRODUCTION()

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
        self.gui.pages[INPUT_PAGE_NAME].disable_additional_options()
        self.load_csv_init()
        self.next_page()
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].select_variables_window(
            range(3,22))
        self.next_page()
        self.next_page()
        self.next_page()
        facet_page = self.gui.pages[FACET_PAGE_NAME]
        facet_page.set_facets_num(2)
        self.on_facet_num_change(None)
        self.gui.button_next.invoke()
        simulate_facets_var_data(FACET_VAR_DATA,
                                 self.gui.pages[
            FACET_VAR_PAGE_NAME].combo_by_var)
        [self.previous_page() for _ in '00005']
        [self.next_page() for _ in '00005']
        try:
            self.output_path = \
                r"C:\Users\Raz_Z\Projects\Shmuel\fssaDist\fssa\tests\dj_csv_test\res\data.fss"
            self.run_fss(self._run_fss)
        except Exception as e:
            print(e)
            raise(e)
        run_file_path = p_FSS_DRV
        # true_file_path = os.path.join(test_dir_path, "FSSAINP.DRV")
        # assert diff_lines_num(run_file_path, true_file_path) == 1
        # assert os.path.exists(self.output_path)
        self.save_session_click(r"C:\Users\Raz_Z\Projects\Shmuel\fssaDist\fssa"
                          r"\tests\dj_load_csv_test\save.mem")
        print(self.gui.pages[
            FACET_VAR_PAGE_NAME].get_all_var_facets_indices())
        print(*self.active_variables_details, sep="\n")

if __name__ == '__main__':
    a = simple_example_gui()
    a.run_process()