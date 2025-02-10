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
SET_MODE_TEST()
# SET_MODE_PRODUCTION()

class dj_csv_test(Controller):
    def __init__(self):
        super().__init__()
        self.gui.pages[START_PAGE_NAME].button_recorded_data.invoke()
        
    def test(self):
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
        # run_file_path = p_FSS_DRV
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if not IS_PRODUCTION():
            self.save_session(os.path.join(current_dir, "test_dj_csv_test.mms"))
            self.reset_session(matrix=False)
            self.load_session(os.path.join(current_dir, "Escape no missing csv.mms"))
            self.gui.pages[INPUT_PAGE_NAME].set_data_file_path(
                os.path.join(current_dir, "Escape-comma delimited-new.csv")
            )
            self.load_csv()
            self.next_page()
            try:
                self.next_page()
            except DataLoadingException as e:
                print("Error loading data. This is expected :)\nAll tests passed")
            
    def test_prod_and_dev(self):
        SET_MODE_PRODUCTION()
        self.test()
        self.reset_session(matrix=False)
        SET_MODE_TEST()
        self.test()
            
if __name__ == '__main__':
    a = dj_csv_test()
    a.test_prod_and_dev()
    a.run_process()