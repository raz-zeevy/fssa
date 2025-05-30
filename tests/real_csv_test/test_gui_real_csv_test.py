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

    def run_recoding(self):
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

    def test_simple_example(self):
        self.gui.pages[START_PAGE_NAME].button_recorded_data.invoke()
        # get the absoult path of the data file
        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(test_dir_path, DATA_PATH)
        self.gui.pages[INPUT_PAGE_NAME].set_data_file_path(data_file_path)
        self.set_header(True)
        self.data_file_extension = ".csv"
        self.load_csv_init()
        self.gui.pages[INPUT_PAGE_NAME].disable_additional_options()
        self.next_page()
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].select_variables_window(
            {i for i in range(3, 21)}
        )
        self.next_page()
        self.run_recoding()
        self.next_page()
        self.next_page()
        try:
            self.output_path = (
                r"C:\Users\raz3z\Projects\Shmuel\fssaDist\fssa\output"
                r"\real_csv.fss"
            )
            self.run_fss(self._run_fss)
            self.enable_view_results()
        except Exception as e:
            print(e)
            raise (e)
        # # run_file_path = p_FSS_DRV
        # # true_file_path = os.path.join(test_dir_path, "FSSAINP.DRV")
        # # assert diff_lines_num(run_file_path, true_file_path) == 1
        assert os.path.isfile(self.output_path)
        # select facets nums to 1
        self.gui.pages[FACET_PAGE_NAME].set_facets_num(1)
        self.on_facet_num_change(None)
        self.next_page()
        self.gui.pages[FACET_VAR_PAGE_NAME].set_facets_vars([[1], [2]])
        mms_path = r"C:\Users\raz3z\Projects\Shmuel\fssaDist\fssa\tests\real_csv_test\mms\facet_1.mms"
        self.save_session(mms_path)
        self.load_session(mms_path)
        self.next_page()
        self.next_page()
        self.run_recoding()
        self.next_page()
        self.next_page()
        self.gui.pages[FACET_PAGE_NAME].set_facets_num(0)
        self.on_facet_num_change(None)
        self.save_session(mms_path)
        self.load_session(mms_path)
        assert not self.facet_var_details, "facet_var_details should be empty"
        assert not self.facet_dim_details, "facet_dim_details should be empty"
        assert not self.facet_details, "facet_details should be empty"


if __name__ == '__main__':
    a = simple_example_gui()
    a.test_simple_example()
    a.run_process()